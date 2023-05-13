# Code used for Adrian's TFM for UAM's Bioinformatics and Computational Biology MSC studies


## ABSTRACT

Cancer is a genetic disease caused by two major factors including inherited variants and somatic alterations. Thanks to the development of sequencing technology, largescale cancer genomics data have been rapidly accumulated. This big data has allowed us to explore the contribution of somatic alterations to the cancer risk. However, the role of cancer-predisposing genes is still unexplored due to the statistical difficulty to detect rare germline variants (Park et al., 2018).  

This study sets a baseline for the identification of novel cancer predisposition genes. A comprehensive set of features that can differentiate previously known CPGs from other genes was collected across genomics, transcriptomics and proteomics. After selecting different groups of features, five different models were trained to compare both selected features’ power and models’ performance.  

This work sets a baseline for future cancer predisposition genes identification. Several suggestions are proposed regarding the different aspects that are treated in this work (feature collection, curation and feature selection and model training) that may be useful to improve the performance on CPG identification.


## OBJECTIVES
The code presented here was used for:
1.	Collecting rare damaging germline variants from TCGA data.
2.	Collecting biological features which could distinguish CPGs from other genes.
3.	Developeng a machine learning model to predict novel CPGs.


## STRUCTURE

* PPI_distances: code used to collect PPI network distances from [STRING](https://string-db.org/) and [HuRI](http://www.interactome-atlas.org/) and compare them.
* PTM_association: code used to collect PRM sites from [UniProtKB](https://www.uniprot.org/), [dPTM](https://awi.cuhk.edu.cn/dbPTM/), [qPTM](http://qptm.omicsbio.info/), [ActiveDriver](https://activedriverdb.org/#:~:text=What%20is%20ActiveDriverDB%3F,genes%2C%20and%20cancer%20driver%20genes.) and [PhosphoSitePlus](https://www.phosphosite.org/homeAction.action), and compute the overlapping bvetween them.
* Tau: code used to compute tissue tau score, which is a measure of specific tissue gene expression.
* feature_selection: code used to obtain the correlation amtrix and random forest classifier used to select features.
* models: code used to define the 5 groups of features used to train the models and train 5 different types of models (dummy, logistic ridge, k-nearest neighbours, support vector classifier and random forest).
* variant_filtering: code used to define the different criteria to be applied during the variant filtering process.
