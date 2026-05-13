FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
COPY 404.html /usr/share/nginx/html/404.html
COPY default.conf /etc/nginx/conf.d/default.conf
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/ || exit 1
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]