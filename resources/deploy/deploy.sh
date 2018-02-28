#!/bin/sh -e

directory=$(mktemp -d)
wget -O- https://github.com/mazerty/$(cat /etc/projectname)/archive/$(cat /etc/stagename).tar.gz | tar -xzf - -C ${directory} --strip 1

while [ ! $(nc postgresql 2501 | grep ok) ]; do sleep 5; done
mvn -f ${directory}/pom.xml flyway:migrate

while [ ! $(nc wildfly 2501 | grep ok) ]; do sleep 5; done
mvn -f ${directory}/pom.xml wildfly:deploy -Dmaven.test.skip=true
