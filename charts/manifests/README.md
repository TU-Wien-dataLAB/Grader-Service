# deploy grader-service

```bash
# ADLS
cd ~/project/adls/grader/grader
kubectl --kubeconfig ../../adls_local_k8s/local.yaml delete ns grader
kubectl --kubeconfig ../../adls_local_k8s/local.yaml create ns grader
# kubectl --kubeconfig ../../adls_local_k8s/local.yaml apply -n grader -f helm/manifests/grader_service_adls_default_image.yaml

kubectl --kubeconfig ../../adls_local_k8s/local.yaml apply -n grader -f helm/manifests/grader_service_adls_build_image.yaml
```

## deploy helm chart
```bash
cd ~/project/adls/grader/grader

helm --kubeconfig ../../adls_local_k8s/local.yaml install --namespace grader --create-namespace grader-service ./helm/grader-service/
```
----
 

################################
services-k8s

submodule

/ 
runner
charts
create new - 
package registery to check

####### dev branch
k8s
app
create a grader directory (grader next to the app) / take the content from devops.
manuly execute

