#!/bin/bash

# Simple Kubernetes Setup Script for Namo
echo "🚀 Setting up Kubernetes for Namo..."

# Install NGINX Ingress Controller
echo "📦 Installing NGINX Ingress Controller..."
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/cloud/deploy.yaml

# Install cert-manager
echo "🔒 Installing cert-manager..."
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.2/cert-manager.yaml

# Wait a bit for cert-manager to be ready
echo "⏳ Waiting for cert-manager to be ready..."
sleep 30

# Create Let's Encrypt ClusterIssuer
echo "🔐 Creating Let's Encrypt ClusterIssuer..."
cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com  # ⚠️ CHANGE THIS TO YOUR EMAIL!
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
EOF

echo "✅ Setup complete!"
echo ""
echo "⚠️  IMPORTANT: Edit the ClusterIssuer above and change 'your-email@example.com' to your actual email!"
echo ""
echo "Next steps:"
echo "1. Set up GitHub secrets (KUBECONFIG, POSTGRES_PASSWORD, SECRET_KEY)"
echo "2. Point grabler.me and api.grabler.me to your cluster's external IP"
echo "3. Push to main branch to deploy"
