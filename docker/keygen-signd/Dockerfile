FROM openeuler/openeuler:22.03
LABEL maintainer="infra@openeuler.org"

# base packages
RUN set -ex ; \
    dnf -y update && \
    dnf -y install shadow
# Create copr-signer:copr-signer manually, so we can
# be sure that the UID and GID is same on all keygen containers
RUN groupadd -r copr-signer -g 992
RUN useradd -r copr-signer -u 993 -g 992 -G 0 -d /var/lib/copr-keygen
RUN mkdir -p /var/lib/copr-keygen/.gnupg && chown copr-signer:copr-signer /var/lib/copr-keygen/.gnupg

# download EUR repo
RUN curl -o /etc/yum.repos.d/eur.repo -L https://eur.openeuler.openatom.cn/coprs/mywaaagh_admin/eur/repo/openeuler-22.03_LTS_SP1/mywaaagh_admin-eur-openeuler-22.03_LTS_SP1.repo

# base packages
RUN set -ex ; \
    dnf -y update && \
    dnf -y install htop \
                   httpd \
                   make \
                   which \
                   wget \
                   vim \
                   yum \
                   sudo \
                   python3-alembic \
                   postgresql-server \
                   redis \
                   tini \
                   obs-signd \
                   && \
    dnf -y install copr-keygen && \
    dnf clean all && rm -rf /var/cache/dnf

# Copy files from the host into the container
COPY files/ /

RUN sed -i 's/Listen 80/#Listen 80/g' /etc/httpd/conf/httpd.conf && \
    sed -i 's/ErrorLog.*/ErrorLog "\/dev\/stdout"/g' /etc/httpd/conf/httpd.conf && \
    sed -i 's/CustomLog.*/CustomLog "\/dev\/stdout" combined/g' /etc/httpd/conf/httpd.conf
# OpenShift runs this project as <RANDOMUID>:root
# Podman runs this as copr-signer with root in supplementary groups
RUN chmod g+rwx /var/log/httpd

# Drop the suid bit
RUN chmod 0755 /usr/bin/sign

# entrypoint needs to have write access here (group=0)
RUN chown copr-signer:root /etc/sign.conf && \
    chmod 0660 /etc/sign.conf

# TODO: we should just check for non-root accounts
RUN sed -i "s|getpass.getuser() != 'copr-signer'|False|" /usr/bin/gpg-copr

RUN dirs="/var/run/signd /var/run/httpd" ; \
    for dir in $dirs; do \
      mkdir -p "$dir" && \
      chown root:root "$dir" && \
      chmod 0770 "$dir" ; \
    done
# setup sudoer for cronjob
RUN echo "copr-signer ALL = (root) NOPASSWD: /etc/cron.daily/copr-keygen" >> /etc/sudoers.d/copr_signer
USER copr-signer
RUN mkdir -p /var/log/copr-keygen && ln -sf /proc/1/fd/1 /var/log/copr-keygen/main.log \
        && ln -sf /proc/1/fd/1 /var/log/copr-keygen/gpg-copr.log

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["/usr/sbin/httpd", "-DFOREGROUND"]
