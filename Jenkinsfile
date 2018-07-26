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

    stage("Deploy") {
        env.STAGE_STATUS="Deploying PGM Service Stacks..."
        sshagent(["dev-swarm-ssh"]) {
            sh "scp -qv -o StrictHostKeyChecking=no pgm-docker-compose.yml root@dev-swarm-master-1:/usr/local/etc/"
        }

        sshagent(["dev-swarm-ssh"]) {
            sh "ssh -qv -o StrictHostKeyChecking=no -l root dev-swarm-master-1 'docker stack deploy -c /usr/local/etc/pgm-docker-compose.yml pgmweb'"
        }
    }
}
