variable "VERSION" {

}

target "base" {
  context = "."
  dockerfile = "Dockerfile"
  platforms = ["linux/amd64", "linux/arm64"]
}

target "nightly" {
  inherits = ["base"]
  tags = ["docker.io/punksecurity/dnsreaper:nightly"]
}

target "release" {
  inherits = ["base"]
  tags = ["docker.io/punksecurity/dnsreaper:${VERSION}", "docker.io/punksecurity/dnsreaper:latest"]
}

target "preview" {
  inherits = ["base"]
  tags = ["docker.io/punksecurity/dnsreaper:preview-${VERSION}"]
}
