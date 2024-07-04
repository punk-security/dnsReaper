import dns
import dns.asyncresolver
import asyncio
import random
import time
import os

import dns.resolver


class DynamicSemaphore:
    def __init__(self, value=1):
        self._lock = asyncio.Lock()

        if value < 0:
            raise ValueError("Semaphore initial value must be >= 0")

        self.value = value

    async def __aenter__(self):
        await self.acquire()
        return None

    async def __aexit__(self, exc_type, exc, tb):
        self.release()

    def locked(self):
        return self.value == 0

    async def acquire(self):
        async with self._lock:
            while self.value <= 0:
                await asyncio.sleep(0.1)

        self.value -= 1
        return True

    def release(self):
        self.value += 1


# We need a semaphore per resolver
# We need a resolver health check
# We need to set a minimum return time of like half a second or something


class Resolver:
    resolutions = 0
    errors = 0
    no_records = 0
    nx_domains = 0

    def __init__(self, parallelism=200, nameservers=[]):
        self.semaphore = asyncio.Semaphore(parallelism)
        if nameservers:
            self.resolvers = []
            for ns in nameservers:
                resolver = dns.asyncresolver.Resolver()
                resolver.nameservers = [ns]
                resolver.cache = dns.resolver.Cache(60 * 60)
                resolver.timeout = 0.5
                resolver.lifetime = 2
                self.resolvers.append(resolver)
        else:
            resolver = dns.asyncresolver.Resolver()
            resolver.cache = dns.resolver.Cache(60 * 60)
            resolver.timeout = 1
            # resolver.lifetime = 1
            self.resolvers = [resolver]

    async def resolve(self, fqdn, type=None):
        async with self.semaphore:
            start = time.time()
            resolver = random.choice(self.resolvers)
            resp = []
            try:
                resp = await resolver.resolve(fqdn, type)
                if self.resolutions % 100 == 0:
                    os.write(2, b".")
                self.resolutions += 1
            except dns.resolver.NoAnswer:
                if self.no_records % 100 == 0:
                    os.write(2, b"-")
                self.no_records += 1
            except dns.resolver.NXDOMAIN:
                if self.nx_domains % 100 == 0:
                    os.write(2, b"+")
                self.nx_domains += 1
            except:
                if self.errors % 100 == 0:
                    os.write(2, b"x")
                self.errors += 1
                # await asyncio.sleep(5) # gash backoff
            time_delta = time.time() - start
            if time_delta < 1:
                await asyncio.sleep(1 - time_delta)
            return resp

    @staticmethod
    async def resolve_with_ns(fqdn, ns, type=None):
        resolver = dns.asyncresolver.Resolver()
        resolver.nameservers = [ns]
        try:
            resp = await resolver.resolve(fqdn, type)
            return resp
        except:
            return []

    @staticmethod
    async def check_health(resolver):
        await resolver.resolve(
            "punksecurity.co.uk",
            "T",
            tcp=True,
        )
