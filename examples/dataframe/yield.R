#!/usr/bin/env Rscript
# Tai Sakuma <sakuma@cern.ch>

##__________________________________________________________________||
suppressPackageStartupMessages(library(dplyr))
suppressPackageStartupMessages(library(gdata))

##__________________________________________________________________||
d1 <-  read.table('tbl_process.txt', header = TRUE)
d1$component <- factor(d1$component, levels = unique(d1$component))
d1$phasespace <- factor(d1$phasespace, levels = unique(d1$phasespace))

d2 <-  read.table('tbl_n_component.met.txt', header = TRUE)
d3 <-  read.table('tbl_nevt.txt', header = TRUE)
d4 <-  read.table('tbl_xsec.txt', header = TRUE)

d <- merge(d1, d2)
d <- d %>% group_by(phasespace, process, met) %>% summarise(n = sum(n), nvar = sum(nvar))
e <- merge(d1, d3)
e <- e %>% group_by(phasespace, process) %>% summarise(nevt = sum(nevt))
e <- merge(e, d4)
d <- merge(d, e)
lumi <- 4000
d$n <- d$n*d$xsec/d$nevt*lumi
d$nvar <- d$nvar*(d$xsec/d$nevt*lumi)^2
d$nevt <- NULL
d$xsec <- NULL
d <- d %>% group_by(process, met) %>% summarise(n = sum(n), nvar = sum(nvar))

d <- d[order(d$process, d$met), ]
write.fwf(as.data.frame(d), 'tbl_out_R.txt')


##__________________________________________________________________||
