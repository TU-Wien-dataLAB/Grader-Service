FROM dtzar/helm-kubectl:latest

# add plugin for helm
# https://github.com/chartmuseum/helm-push/#readme
RUN helm plugin install https://github.com/chartmuseum/helm-push

WORKDIR /config

CMD bash
