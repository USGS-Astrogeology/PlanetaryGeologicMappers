node("alpine") {
  stage("Checkout") {
      sh "apk add git openssh rsync"
      checkout scm
  }

  stage("Deploy") {
    sshagent(['dmz-swarm']) {
      sh '''
        rsync -a --progress -e 'ssh -q -o StrictHostKeyChecking=no -l jenkins' . dmz-swarm-master-1:/usr/local/etc/pgm/
        ssh jenkins@dmz-swarm-master-1 docker stack deploy -c /usr/local/etc/pgm/pgm-docker-compose.yml pgm
      '''
    }
  }

}
