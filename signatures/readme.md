# Signatures

Signatures in this directory are auto-imported into the scanning engine.  The scanning engine then checks every domain with every signature, unless that signature is excluded from the scan due to its ```CONFIDENCE``` or name.

Each signature has to inherit from the [Base Class](templates/base.py)

Most signatures inherit from another template class, which is meant to standardise their implementation.

We heavily test signatures using the pytest framework, testing that they work as expected with dummy and live checks.

Each signature has two components, a ```potential``` function and a ```check``` function.  This is to reduce the processing time and number of active checks, such as DNS and web queries.

The potential function is used to identify if this signature might be relevant for this domain, and typically should not contain any active check such as a web request or DNS request.  We try to only check data we already have, such as pattern matching the cnames.

The check function is used to validate the takeover and will only run if the domain has passed the potential function.  This check can be slower / more intensive as it wont run for every domain.

## Adding a new signature

It is probably best copying another signature that resembles the one you are looking to implement.  This also reduces or negates the need for you to add your own tests.

If a signature uses a standard template such as [cname_found_but_string_in_body](templates/cname_found_but_string_in_body.py) then there are no further tests required.

If you need to use a custom approach, you should use the components in the [checks](checks/) directory.  These are sorted by the domain component you are testing.  These checks are all havily tested for edge cases.  If you need to add a new check component, ensure you add the relevant edge case tests.