---
title: "Deploying Self-hosted Microbin on Rocky Linux 9"
date: 2024-08-31
author: Muhammad Najmi bin Ahmad Zabidi
---

### Self-Hosted Microbin on Rocky Linux 9

**Note**: This write-up was based on the installation done on Rocky Linux 9. You may need to adjust this example accordingly with other distros with their specific command.

In the world of data sharing and collaboration between our team members and the public, secure and efficient ways to share text and files are essential. While there are many cloud-based options available, some might prefer to keep their data in their own hands. If you're one of those individuals, Microbin might be just the solution you're looking for.

### What is Microbin?

Microbin is a Rust-based software that acts as a self-hosted "pastebin" alternative. It allows users to share publicly accessible text or encrypted text files, putting you in control of your data sharing needs. Users can choose whether to share the data/text publicly or privately. It also has syntax highlighting capabilities.

### Installation Options

There are several ways to install Microbin. In this case, we will install it directly on a Rocky Linux server. You might need to install `git`, Rust packages, and `cargo` before starting.

#### Cargo

For those comfortable with Rust and its package manager, Cargo, installing Microbin is a breeze. Simply use the following command as mentioned [here](https://microbin.eu/docs/installation-and-configuration/cargo):

```bash
cargo install microbin
```

### Troubleshooting
If you encounter the following error:

```
Can't locate FindBin.pm in @INC (you may need to install the FindBin module) (@INC contains: /usr/local/lib64/perl5/5.32 /usr/local/share/perl5/5.32 /usr/lib64/perl5/vendor_perl /usr/share/perl5/vendor_perl /usr/lib64/perl5 /usr/share/perl5) at ./Configure line 15.
BEGIN failed--compilation aborted at ./Configure line 15.
thread 'main' panicked at /home/microbin/.cargo/registry/src/index.crates.io-6f17d22bba15001f/openssl-src-300.3.1+3.3.1/src/lib.rs:621:9:
```

You can troubleshoot by installing the related Perl package:
```.bash
dnf install perl-FindBin
```

Another issue which I encounter was:
```
Error configuring OpenSSL build:
    Command: cd "/tmp/cargo-installcFs6oN/release/build/openssl-sys-d3d75fe094af940b/out/openssl-build/build/src" && env -u CROSS_COMPILE AR="ar" CC="cc" RANLIB="ranlib" "perl" "./Configure" "--prefix=/tmp/cargo-installcFs6oN/release/build/openssl-sys-d3d75fe094af940b/out/openssl-build/install" "--openssldir=/usr/local/ssl" "no-dso" "no-shared" "no-ssl3" "no-tests" "no-comp" "no-zlib" "no-zlib-dynamic" "--libdir=lib" "no-md2" "no-rc5" "no-weak-ssl-ciphers" "no-camellia" "no-idea" "no-seed" "linux-x86_64" "-O2" "-ffunction-sections" "-fdata-sections" "-fPIC" "-m64"
    Exit status: exit status: 2
```

This build issue was resolved by installing the `perl-core` package:
```bash
dnf install perl-core
```

Please note that these errors were encountered during the installation on Rocky Linux 9 using the minimal ISO. The complete installer ISO might already include these Perl dependencies.


### Installing on Rocky Linux
Once you've chosen your installation method, you'll want to get Microbin up and running on your Linux machine. The process is similar regardless of your choice, but let's assume you've gone with the Cargo installation for this example.

### Create a systemd service
To ensure Microbin starts upon system boot, create a systemd service unit file. In this case, we will run the Microbin service under the local `microbin` user. Please refer to the [documentation](https://microbin.eu/docs/installation-and-configuration/cargo/) for assigning environment variables as needed.

Let's say the port that was chosen is port 2999, then can put the parameter 
```
Environment="MICROBIN_PORT=2999"
```

inside the  ` /etc/systemd/system/microbin.service` file.

The other important parameters are:

```
User=microbin
Group=microbin
ExecStart=/home/microbin/.cargo/bin/microbin
```

since we are using the `microbin` user account for this web application.

We can quickly start the microbin service after we saved the file with:

```
systemctl enable microbin --now 
```

### Proxying with Apache httpd
To make Microbin accessible over the standard HTTP and HTTPS ports (80 and 443), you can set up a reverse proxy with Apache httpd. Here's a brief guide on how to do that:

- Install Apache httpd:

```.bash
dnf install httpd

```

- Create a Virtual Host Configuration:
Create a new Apache configuration file for Microbin, let’s say in `/etc/httpd/conf.d/microbin.conf`.
Add the following lines to configure the reverse proxy:

```bash
<VirtualHost *:80>
    ServerName microbin.example.com
    ProxyPass / http://127.0.0.1:2999/
    ProxyPassReverse / http://127.0.0.1:2999/
</VirtualHost>
```

Later, you can extend and adjust the virtual host configuration for port 443 to include the SSL cert path and cipher packs setting accordingly.

- Enable and Start Apache:

```bash
systemctl enable httpd --now
```

Now, Microbin should be accessible through your Rocky Linux VM via Apache httpd on ports 80 and 443.
If, you have not be able to see it yet, let's go through the Rocky Linux 9's firewall settings.

### Adjust Firewall Settings

Just in case the when you type `iptables -vL` as `root` and nothing seems blocking the port, you may need to consider to go through the `firewall-cmd` rules

- Check first:

```.bash
firewall-cmd --list-all
```

- Then open the related ports:

```.bash
firewall-cmd --permanent --add-port=80/tcp
firewall-cmd --permanent --add-port=443/tcp
firewall-cmd --reload
```

- Verify the changes:

```.bash
firewall-cmd --list-all
```

### SELinux
Just in case you found that starting the `httpd` service doesn't show the pages, you can parse the output of `/var/log/audit/audit.log`. For a starting you may need to put SELinux into permissive first with `setenforce 0`. Later you can check the problematic lines with `grep AVC /var/log/audit/audit.log|audit2why`.

### Conclusion
The simple setup described is for public pastes and does not include secret/encrypted file sharing. Please refer to the official documentation for more details.

In conclusion, Microbin is a powerful and flexible self-hosted pastebin alternative that can help you share text and files. With installation options for Cargo, Docker, and source code, it adapts to your preferences. By using Rocky Linux, a systemd service, and Apache httpd, you can create a robust, self-hosted data sharing solution. Enjoy the convenience of pastebin-like functionality with complete control over your data.



