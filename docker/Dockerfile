# Pull base image.
FROM ubuntu:18.04
## Update OS
RUN \
  sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list && \
  apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y build-essential && \
  apt-get install -y software-properties-common && \
  apt-get install -y byobu curl htop man unzip vim wget iputils-ping && \
  rm -rf /var/lib/apt/lists/*


 # Java Version
 ENV JAVA_VERSION_MAJOR 8
 ENV JAVA_VERSION_MINOR 201
 ENV JAVA_VERSION_BUILD 09
 ENV JAVA_PACKAGE       jdk

 # Download and unarchive Java
 RUN mkdir -p /opt && curl -jksSLH "Cookie: oraclelicense=accept-securebackup-cookie" \
   http://download.oracle.com/otn-pub/java/jdk/${JAVA_VERSION_MAJOR}u${JAVA_VERSION_MINOR}-b${JAVA_VERSION_BUILD}/42970487e3af4f5aa5bca3f542482c60/${JAVA_PACKAGE}-${JAVA_VERSION_MAJOR}u${JAVA_VERSION_MINOR}-linux-x64.tar.gz \
     | tar -xzf - -C /opt &&\
     ln -s /opt/jdk1.${JAVA_VERSION_MAJOR}.0_${JAVA_VERSION_MINOR} /opt/jdk &&\
     rm -rf /opt/jdk/*src.zip \
            /opt/jdk/lib/missioncontrol \
            /opt/jdk/lib/visualvm \
            /opt/jdk/lib/*javafx* \
            /opt/jdk/jre/lib/plugin.jar \
            /opt/jdk/jre/lib/ext/jfxrt.jar \
            /opt/jdk/jre/bin/javaws \
            /opt/jdk/jre/lib/javaws.jar \
            /opt/jdk/jre/lib/desktop \
            /opt/jdk/jre/plugin \
            /opt/jdk/jre/lib/deploy* \
            /opt/jdk/jre/lib/*javafx* \
            /opt/jdk/jre/lib/*jfx* \
            /opt/jdk/jre/lib/amd64/libdecora_sse.so \
            /opt/jdk/jre/lib/amd64/libprism_*.so \
            /opt/jdk/jre/lib/amd64/libfxplugins.so \
            /opt/jdk/jre/lib/amd64/libglass.so \
            /opt/jdk/jre/lib/amd64/libgstreamer-lite.so \
            /opt/jdk/jre/lib/amd64/libjavafx*.so \
            /opt/jdk/jre/lib/amd64/libjfx*.so

 # Set environment
 ENV JAVA_HOME /opt/jdk
 ENV PATH ${PATH}:${JAVA_HOME}/bin


# download Java Cryptography Extension
RUN cd /tmp/ && \
    curl -LO "http://download.oracle.com/otn-pub/java/jce/8/jce_policy-8.zip" -H 'Cookie: oraclelicense=accept-securebackup-cookie' && \
    unzip jce_policy-8.zip && \
    rm jce_policy-8.zip && \
    yes |cp -v /tmp/UnlimitedJCEPolicyJDK8/*.jar ${JAVA_HOME}/jre/lib/security/

# Define commonly used JAVA_HOME variable
ENV JAVA_HOME /usr/lib/jvm/java-8-oracle

# Create the home dir
RUN mkdir -p /opt/shopalitic/home

# Define working directory.
WORKDIR /opt/shopalitic/home

# Build this project
COPY target/hellospring-*-SNAPSHOT.jar  	/opt/shopalitic/home/hellospring-api.jar


# Define default command.
RUN chmod 700 /opt/shopalitic/home/hellospring-api.jar

ENTRYPOINT ["java","-jar","/opt/shopalitic/home/hellospring-api.jar"]
CMD ["-h"]
