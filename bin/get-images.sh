oc get imagestreams -o json | jq -r '.items[] | {imageStream:.metadata.name, image:.status.tags[]?.items[].image} | (.imageStream + "@" + .image)' | xargs -I {} oc get 'imagestreamimage/{}' -o json |  jq -r '.image.dockerImageLayers[] | {name: .name, size: .size}' | jq -sr 'unique_by(.name) | .[].size' | awk '{ sum += $1 } END { print (sum / 1024 / 1024 / 1024) "GB" }'