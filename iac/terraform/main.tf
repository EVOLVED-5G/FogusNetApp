resource "kubernetes_pod" "Siem5g" {
  metadata {
    name = "Siem5g"
    namespace = "evolved5g"
    labels = {
      app = "Siem5g"
    }
  }

  spec {
    container {
      image = "dockerhub.hi.inet/evolved-5g/dummy-netapp:latest"
      name  = "dummy-netapp"
    }
  }
}

resource "kubernetes_service" "Siem5g_service" {
  metadata {
    name = "Siem5g"
    namespace = "evolved5g"
  }
  spec {
    selector = {
      app = kubernetes_pod.Siem5g.metadata.0.labels.app
    }
    port {
      port = 8080
      target_port = 8080
    }
  }
}
