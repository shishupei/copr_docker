FROM openeuler/openeuler:22.03
LABEL maintainer="infra@openeuler.org"

# TERM is to make the tito work in container, rhbz#1733043
ENV TERM=linux
ENV PYTHONPATH=/usr/share/copr/

# download EUR repo
RUN curl -o /etc/yum.repos.d/eur.repo -L https://eur.openeuler.openatom.cn/coprs/mywaaagh_admin/eur/repo/openeuler-22.03_LTS_SP1/mywaaagh_admin-eur-openeuler-22.03_LTS_SP1.repo

# base packages
RUN set -ex ; \
    dnf -y update && \
    dnf -y install htop \
                   which \
                   wget \
                   vim \
                   cgit \
                   python3-rpkg-1.65 \
                   python3-ipdb \
                   tini \
                   && \
    dnf -y install copr-dist-git sudo && \
    dnf clean all && rm -rf /var/cache/dnf

RUN rm /etc/httpd/conf.d/ssl.conf

RUN echo "AliasMatch \"/repo(/.*)/md5(/.*)\" \"/var/lib/dist-git/cache/lookaside\\$1\\$2\"" >> /etc/httpd/conf.d/dist-git/lookaside-copr.conf && \
    echo "Alias /repo/ /var/lib/dist-git/cache/lookaside/" >>  /etc/httpd/conf.d/dist-git/lookaside-copr.conf

RUN sed -i 's/Listen 80/Listen 5001/' /etc/httpd/conf/httpd.conf && \
    sed -i 's/ErrorLog.*/ErrorLog "\/dev\/stdout"/g' /etc/httpd/conf/httpd.conf && \
    sed -i 's/CustomLog.*/CustomLog "\/dev\/stdout" combined/g' /etc/httpd/conf/httpd.conf && \
    sed -i 's|Fedora Release Engineering|openEuler infrastructure|g' /etc/dist-git/dist-git.conf && \
    sed -i 's|rel-eng@lists.fedoraproject.org|infra@openeuler.org|g' /etc/dist-git/dist-git.conf

RUN mkdir /tmp/copr-dist-git
RUN chown copr-dist-git:packager /tmp/copr-dist-git

# copy filesystem setup and setup ownership and permissions
COPY files/ /
RUN chmod 644 /etc/copr/copr-dist-git.conf && chmod 755 /copr-dist-git-assure-perm

RUN echo " [user]" >> /home/copr-dist-git/.gitconfig && \
    echo " email = infra@openeuler.org" >> /home/copr-dist-git/.gitconfig && \
    echo " name = Copr dist git" >> /home/copr-dist-git/.gitconfig && \
    chown copr-dist-git:copr-dist-git /home/copr-dist-git/.gitconfig /var/log/copr-dist-git

RUN sed -i "s/^cache-size.*//" /etc/cgitrc
RUN echo 'scan-path=/var/lib/dist-git/git/rpms' | tee -a /etc/cgitrc
RUN echo 'include=/var/lib/dist-git/cache/cgit/repo-configuration.rc' | tee -a /etc/cgitrc
RUN mkdir -p /var/lib/dist-git/cache/cgit/ && chown apache:root /var/lib/dist-git/cache/cgit

RUN directories="/etc/httpd /var/run/httpd /var/log/httpd /var/lib/dist-git /run/lock" ; \
    chown -R copr-dist-git:root $directories && \
    chmod -R g+rwX $directories

RUN echo "copr-dist-git ALL = (root) NOPASSWD: /copr-dist-git-assure-perm,/etc/cron.monthly/copr-dist-git" >> /etc/sudoers.d/copr-dist-git
RUN patch /usr/lib/python3.9/site-packages/copr_common/redis_helpers.py < /redis_helpers.patch
RUN patch /usr/lib/python3.9/site-packages/copr_dist_git/helpers.py < /helpers.patch
USER copr-dist-git

RUN ln -sf /proc/1/fd/1 /var/log/copr-dist-git/main.log

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["bash", "-c", "mkdir -p /var/lib/dist-git/cache /var/lib/dist-git/git && sudo /copr-dist-git-assure-perm && exec /usr/bin/copr-run-dispatcher imports"]
