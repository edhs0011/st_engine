FROM i-registry.consumervpn.trendmicro.com/st_engine-runbase

RUN mkdir /st_engine

COPY . /st_engine

WORKDIR /st_engine/st_engine