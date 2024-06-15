#!/bin/bash
set -e

manifest_file="./custom_components/thermia/manifest.json"

latest_version=ThermiaOnlineAPI==$(lastversion ThermiaOnlineAPI --at pip)

echo "Last version of ThermiaOnlineAPI: $latest_version"

current_version=$(jq '.requirements[0]' $manifest_file | tr -d '"')

echo "Current version of ThermiaOnlineAPI: $current_version"

if [ "$current_version" != "$latest_version" ]; then
  echo "Updating version to $latest_version"
  version=$latest_version jq ".requirements = [env.version]" $manifest_file > tmp.$$.json && mv tmp.$$.json $manifest_file
  echo "ThermiaOnlineAPI version updated to $latest_version"
  echo "LATEST_API_VERSION=$latest_version" >> $GITHUB_ENV
else
  echo "Version $current_version is already up to date"
fi
