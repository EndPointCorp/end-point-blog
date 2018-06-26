---
author: Jon Jensen
title: "SRV DNS records in Terraform and Cloudflare"
tags: devops, terraform, cloud, hosting
gh_issue_number: 1437
---

<img src="/blog/2018/06/26/srv-dns-terraform-cloudflare/2109300822_07103c8f1a_o-crop.jpg" alt="woman walking across train tracks" /><br>[(Photo by David Goehring, CC BY 2.0, cropped)](https://www.flickr.com/photos/carbonnyc/2109300822/)

At End Point we are using [Terraform](https://www.terraform.io/) for a few clients to manage their web hosting [infrastructure as code (IaC)](https://en.wikipedia.org/wiki/Infrastructure_as_Code). Terraform is particularly helpful when working with multiple cloud or infrastructure providers and stitching together their services.

For example, for one web application that involves failover from the primary production infrastructure to a secondary location at a different provider, we are using [Cloudflare](https://www.cloudflare.com/) as a CDN to provide caching, DDoS mitigation, and traffic routing in front of virtual servers at DigitalOcean and Amazon Web Services (AWS).

We decided we wanted to store all of their infrastructure configuration in Terraform, not just what is required for the web application, so we can recreate their entire infrastructure from their Git repository.

This all went fine until we got to their email DNS records. Our client is using Microsoft Office 365 for their email, which requires some SRV records. Terraform’s Cloudflare provider works fine with the universal MX records, but when we first wanted to do this, the Terraform provider for Cloudflare did not support SRV records at all.

Luckily for us, Terraform recently (6 April 2018) gained support for DNS SRV records as mentioned in the [release notes](https://github.com/terraform-providers/terraform-provider-cloudflare/blob/master/CHANGELOG.md#100-april-06-2018) and described in more detail in the [pull request](https://github.com/terraform-providers/terraform-provider-cloudflare/pull/29) that added the feature.

Great! So now we can get on with this.

I began by naively assuming that the SRV record data should be given in space-separated form like many DNS interfaces use, including BIND and Cloudflare’s web interface itself. I tried setting it like this:

```
resource "cloudflare_record" "_sipfederationtls_tcp" {
  domain = "${var.domain}"
  name   = "_sip._tcp.${var.subdomain}"
  type   = "SRV"
  value  = "100 1 443 sipdir.online.lync.com."
}
```

But that resulted in an error. So when in doubt, consult the documentation, right? I did that:

* [Terraform Cloudflare provider docs](https://www.terraform.io/docs/providers/cloudflare/r/record.html#data)
* [Cloudflare API docs](https://api.cloudflare.com/#dns-records-for-a-zone-update-dns-record)

Those make it clear that a `data` element is required, but give no indication what format is needed.

This is not currently documented for Cloudflare’s API, nor for Terraform’s Cloudflare provider. User [EpiqSty helpfully recorded](https://github.com/terraform-providers/terraform-provider-cloudflare/pull/29#issuecomment-374600386) asking Cloudflare’s support, who recommended reverse-engineering the format:

> In the meantime, what I would suggest is you can create a SRV record via our UI and then you can use the API to do a GET request on the DNS records, that should show you all the fields that are required.

Ok, then!

It turns out that we must provide the component parts of the SRV record disassembled in key/​value pairs as the Cloudflare API expects, which looks like this in Terraform config:

```
resource "cloudflare_record" "_sip_tls" {
  domain = "${var.domain}"
  name   = "_sip._tls.${var.subdomain}"
  type   = "SRV"
  data   = {
    service  = "_sip"
    proto    = "_tls"
    name     = "${var.subdomain}."
    priority = 100
    weight   = 1
    port     = 443
    target   = "sipdir.online.lync.com."
  }
}
```

One unexpected aspect of this is that it requires duplicating the parts that make up the `name` although the name doesn’t seem to be used by Cloudflare, which assembles the name from the `data` components `service`, `proto`, and `name`. The `name` is apparently just there for Terraform, unlike other DNS records where the name is used as the DNS record value.

The Terraform Cloudflare provider also gained support for the much more obscure [DNS LOC record type](https://en.wikipedia.org/wiki/LOC_record) at the same time, and it works similarly.

Thanks to [Ben Vickers](https://github.com/benjvi) who contributed the new feature to Terraform!
