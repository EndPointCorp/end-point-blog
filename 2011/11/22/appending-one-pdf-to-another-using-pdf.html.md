---
author: Brian Buchalter
gh_issue_number: 514
tags: tips, tools
title: Appending one PDF to another using PDF Toolkit
---



Ever need to manipulate PDFs?  Prefer the command line? Us too.  Imagine you have a contract in PDF format.  When people print, sign, and re-scan the contract, that's good documentation of the signature, but the clarity of the original machine-readable text is lost and the the file's size is unnecessarily large.  One solution is to append the scanned signature page to the original contract document.

There are many PDF editors out there which address this need.  One command line solution that works well is PDF Labs's [PDF Toolkit](http://www.pdflabs.com/docs/pdftk-man-page/).  Let's look at how we would use PDF Toolkit to append one document to another.

```bash
pdftk contract.pdf scanned_contract.pdf cat output original_and_signed_contract.pdf
```

With this command we now have both contracts in their entirety.  What we really want is to just take the signature page and append it.  Let's revise our command a bit to only take the signature page using what PDF Toolkit calls handles.

```bash
pdftk A=contract.pdf B=scanned_contract.pdf cat A B5 output contract_with_signature_attached.pdf
```

We've assigned each document to a handle (A and B), which allows us to define the order of the output as well as the pages we want to select for the output.  With the argument B5 PDF Toolkit knows we only want the fifth page of the scanned_contract.pdf.  Ranges are also supported, so we could write something like B4-5 too.

Unfortunately, the scanned contract was scanned upside down, so let's rotate 180 degrees by adding the -endS argument.

```bash
pdftk A=contract.pdf B=scanned_contract.pdf cat A B5-endS output contract_with_signature_attached.pdf
```

One notable issue I encountered while rotating individual pages was the inability to rotate and append only the first page.  When specifying an option like B1-endS, the entire "B" document would be rotated and appended instead of just the first page. One other gotcha to remember: escape spaces and special characters when providing the names of documents.  For example, if our document was named "scanned contract.pdf" we would need to do this:

```bash
pdftk contract.pdf scanned\ contract.pdf cat output signed_contract.pdf
```

The PDF Toolkit is licensed under GNU General Public License (GPL) Version 2.  PDF Labs's website provides a host of other [examples](http://www.pdflabs.com/docs/pdftk-cli-examples/) including how to encrypt, password-protect, and repair PDFs.


