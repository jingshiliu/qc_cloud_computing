FROM amazonlinux:2

RUN yum update -y && \
    yum install -y curl && \
    curl -sL https://rpm.nodesource.com/setup_14.x | bash - && \
    yum install -y nodejs && \
    yum clean all

WORKDIR /app

COPY package.json yarn.lock ./

RUN curl -sS https://dl.yarnpkg.com/rpm/yarn.repo | tee /etc/yum.repos.d/yarn.repo && \
    rpm --import https://dl.yarnpkg.com/rpm/pubkey.gpg && \
    yum install -y yarn && \
    yarn install --production && \
    yum remove -y yarn && \
    yum clean all

COPY . .

CMD ["node", "./src/index.js"]
