#!/usr/bin/env bash
set -euo pipefail

IMAGE="${1:-parameta/devops-mvp:latest}"
KUBECTL_CONTEXT="${KUBECTL_CONTEXT:-}" # optional context override

if [[ -n "$KUBECTL_CONTEXT" ]]; then
  KUBECTL_CMD=(kubectl --context "$KUBECTL_CONTEXT")
else
  KUBECTL_CMD=(kubectl)
fi

printf 'Applying Kubernetes manifests...\n'
"${KUBECTL_CMD[@]}" apply -f k8s/

printf 'Updating deployment image to %s...\n' "$IMAGE"
"${KUBECTL_CMD[@]}" set image deployment/parameta-devops-mvp app="$IMAGE"

printf 'Waiting for rollout to finish...\n'
"${KUBECTL_CMD[@]}" rollout status deployment/parameta-devops-mvp
