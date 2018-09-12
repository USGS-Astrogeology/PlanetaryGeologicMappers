@Library("astroitops") _

buildNotifier{
    stage("Checkout") {
        checkout scm
    }

    stage("Build") {
        docker.withRegistry("http://registry.hub.docker.com", "sakins-dockerhub") {
            def app = docker.build("usgsastro/planetarygeologicmappers")
            app.push("latest")
        }
    }
}
