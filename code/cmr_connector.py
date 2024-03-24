import ast
import datetime
import json
import os
from typing import Dict, List, Union

import dotenv
from chains import (
    CMRSummarizeChain,
    CombinedQAChain,
    DatetimeChain,
    DatetimeLocationFinderChain,
    EvidenceSelectorChain,
    QASummarizeChain,
    SingleQAChain,
)
from prompting_tools import GCMDKeywordSearchTool, geocode


class CMRConnector:
    def __init__(self, *args, **kwargs):
        dotenv.load_dotenv()
        self.keyword_searcher = GCMDKeywordSearchTool()
        self.dtl_finder = DatetimeLocationFinderChain()
        self.dt_formatter = DatetimeChain()
        self.single_context_qa = SingleQAChain(model_name=kwargs["singleqa_model"]) if "singleqa_model" in kwargs else SingleQAChain() #NOQA: E501
        self.qa_summarizer = QASummarizeChain()
        self.cmr_summarizer = CMRSummarizeChain()
        self.evidence_selector = EvidenceSelectorChain()
        self.multi_context_qa = CombinedQAChain()

    def get_dt_location(
        self,
        text,
    ):
        response = self.dtl_finder.run(text).strip()
        parsed_tuple = ast.literal_eval(response)
        datetime_cmr = (
            self.dt_formatter.run(parsed_tuple[0]) if parsed_tuple[0] else None
        )
        location_cmr = geocode(parsed_tuple[1]) if parsed_tuple[1] else None
        results = {
            "datetime": parsed_tuple[0],
            "location": parsed_tuple[1],
            "datetime_cmr": datetime_cmr,
            "datetime_start_end": datetime_cmr.strip("temporal[]=")
            if datetime_cmr
            else None,
            "location_cmr": location_cmr,
            "location_bbox": location_cmr.strip("bounding_box[]=")
            if location_cmr
            else None,
        }

        return results

    def get_keywords(self, text):
        return {
            "keyword": self.keyword_searcher.get_formatted_science_kws(text),
            "keyword_cmr": self.keyword_searcher.get_science_kws(text),
        }

    def qa_summarize(self, query: str, contexts: List[str], parse_to_dict=True) -> str:
        contexts = list(set(contexts))
        inputs = {
            "query": query,
            "contexts": contexts,
        }
        summary_answer = self.qa_summarizer.run(inputs)
        return (
            summary_answer
            if not parse_to_dict
            else self.parse_summarizer(summary_answer)
        )

    def reader(self, query: str, context: str, parse_to_dict=True) -> Union[str, dict]:
        inputs = {
            "query": query,
            "context": context,
        }
        answer_reference = self.single_context_qa.run(inputs)
        return (
            answer_reference
            if not parse_to_dict
            else self.parse_singleqa(answer_reference)
        )

    def multi_reader(
        self, query: str, contexts: List[str],
    ) -> Union[str, dict]:
        inputs = {
            "query": query,
            "contexts": contexts,
        }
        answer_reference = self.multi_context_qa.run(inputs)
        parsed_answer = self.parse_singleqa(answer_reference)
        
        matching_context_id = -1
        
        for i, context in enumerate(contexts):
            
            if "evidence" in parsed_answer.keys():
                # extract text between quotes
                evidence = parsed_answer["evidence"]
                evidence = evidence[evidence.find('"')+1:evidence.rfind('"')].strip()
                
                if evidence.lower() in context.strip().lower():
                    matching_context_id = i
        parsed_answer.update({"matching_context_id": matching_context_id})
        return parsed_answer
    
    def evidence_select(
        self,
        query: str,
        reader_response_list: List[Dict[str, str]],
    ) -> str:
        inputs = {
            "query": query,
            "evidences": [r["evidence"] for r in reader_response_list if "N/A" not in [r["evidence"], r["answer"]]],
        }
        matching_evidence = self.evidence_selector.run(inputs)
        for reader_response in reader_response_list:
            if matching_evidence.strip().lower() in reader_response["evidence"].strip().lower():
                return reader_response
        return "No matching evidence found"


    @staticmethod
    def parse_summarizer(text: str) -> str:
        try:
            reference = text.split("Reference: ")[-1]
            answer = text.split("Reference: ")[0].split("Answer: ")[-1]
            summary = text.split("Answer: ")[0].split("Summary: ")[-1]

        except IndexError:
            answer = None
            summary = None
            reference = None
        return {"answer": answer, "summary": summary, "reference": reference}

    @staticmethod
    def parse_singleqa(text: str) -> str:
        try:
            evidence = text.split("Evidence: ")[-1]
            answer = text.split("Evidence: ")[0].split("Answer: ")[-1]

        except IndexError:
            answer = text
            evidence = None

        return {"answer": answer, "evidence": evidence}

    def cmr_summarize(
        self, query: str, cmr_responses: Union[Dict, str], max_cmr_items: str = 5
    ) -> str:
        def filter_cmr_item(cmr_item, max_abstract_sentences=2):
            sents = cmr_item["umm"]["Abstract"].split(".")
            max_abstract_sentences = min(max_abstract_sentences, len(sents))
            abstract = " ".join(sents)
            return {
                "EntryTitle": cmr_item["umm"]["EntryTitle"],
                "Abstract": abstract,
            }

        if isinstance(cmr_responses, str):
            cmr_responses = json.loads(cmr_responses)
        assert isinstance(cmr_responses, dict)
        filtered_responses = dict()
        filtered_responses["hits"] = cmr_responses["hits"]
        filtered_responses = [
            filter_cmr_item(cmr_item)
            for cmr_item in cmr_responses["items"][:max_cmr_items]
        ]
        inputs = {
            "query": query,
            "cmr_responses": filtered_responses,
        }
        return self.cmr_summarizer.run(inputs)


if __name__ == "__main__":
    cmr_connector = CMRConnector()
    # text = "I want to find all the datasets that contain aerosol data from 2010 to 2015 in the US"
    # print(cmr_connector.get_dt_location(text))
    # print(cmr_connector.get_keywords(text))
    # print(
    #     cmr_connector.qa_summarize("What is the answer to life?", ["42", "life is 42"])
    # )
    # print(
    #     cmr_connector.qa_summarize("What is the answer to life?", ["42", "life is 42"])
    # )
    # cmr_json = json.load(open("../data/sample_cmr_response.json"))
    # print(
    #     cmr_connector.cmr_summarize("Monitor forest fires for the year 2020", cmr_json)
    # )
    query = 'What products does the HLS suite contain?'
    contexts = ["when possible. For HLS dates without a coincident reference label, if the closest preceding and following reference date have the same label, this is compared with the DIST_ALERT label. If the two reference dates have different labels this time step is excluded as it is unknown when the disturbance occurred between these two dates. Given that the validation assessment covers an entire year with all HLS acquisition dates evaluated, all seasons are assessed and any errors due to intra-annual variation will be quantified. Figure 13. Example validation data from ~3-4m PlanetScope imagery over a residential expansion site near Dallas, Texas. From left to right, image from 12-31-2019, image from 12-29-2020, and mapped vegetation loss in black overlay. All cloud-free PlanetScope data (not shown here) will be used to refine data of disturbance estimation. Sample 30m HLS pixel shown in red outline exhibits vegetation loss. The DIST_ALERT has two types of disturbances: provisional and confirmed. Both types of disturbances in DIST_ALERT will be evaluated against the high-resolution derived time-series. Typically, the confirmed disturbances in the DIST_ALERT product are expected to have a higher accuracy as they have been repeatedly observed. However, given that for minimum latency DIST_ALERT products may be used as soon as HLS scenes are characterized and before a new disturbance can be confirmed from repeat observations, we will also validate provisional alerts. The overall user's and producer's accuracies of both products will be reported and provide a globally representative measure of DIST product performance. The assessment of the vegetation cover indicator layer pertains to the vegetation layers of the DIST suite used as inputs to the disturbance detection algorithms and distributed with the DIST product. Although this layer is without a formal requirement, providing a general assessment of this intermediate layer's utility is valuable for users and for", 'The objective is to provide the MODIS land products at consistent low resolution spa- tial and temporal scales suitable for global modeling. In practice, there is a fair amount of variation in the spatial and temporal gridding conventions used among the MODIS land CMG products. 3.1.4 Collections Reprocessing of the entire MODIS data archive is periodically performed to incorporate better cali- bration, algorithm refinements, and improved upstream data into all MODIS products. The updated MODIS data archive resulting from each reprocessing is referred to as a collection. Later collections supersede all earlier collections. For the Terra MODIS, Collection 1 consisted of the first products generated following launch. Terra MODIS data were reprocessed for the first time in June 2001 to produce Collection 3. (Note that this first reprocessing was numbered Collection 3 rather than, as one would expect, Collec- tion 2.) Collection 3 was also the first version produced for the Aqua MODIS products. Collec- tion 4 reprocessing began in December 2002 and was terminated in December 2006. Production of the Collection 5 products commenced in mid-2006. Production of the "Tier-1" Collection 6 MODIS products, which includes the active fire products, commenced in February 2015 and will continue through 31 December 2021. Production of the MODIS product suite will at that point continue via the Collection 6.1 "mini-reprocessing" that was initiated for the land products in late 2020. 3.2 Level 2 Fire Products: MOD14 (Terra) and MYD14 (Aqua) This is the most basic fire product in which active fires and other thermal anomalies, such as volca- noes, are identified. The Level 2 product is defined in the MODIS orbit geometry covering an area of approximately 2340 x 2030 km in the along-scan and along-track directions, respectively. It is used to generate all of the higher-level fire products, and contains the', 'The objective is to provide the MODIS land products at consistent low resolution spa- tial and temporal scales suitable for global modeling. In practice, there is a fair amount of variation in the spatial and temporal gridding conventions used among the MODIS land CMG products. 3.1.4 Collections Reprocessing of the entire MODIS data archive is periodically performed to incorporate better cali- bration, algorithm refinements, and improved upstream data into all MODIS products. The updated MODIS data archive resulting from each reprocessing is referred to as a collection. Later collections supersede all earlier collections. For the Terra MODIS, Collection 1 consisted of the first products generated following launch. Terra MODIS data were reprocessed for the first time in June 2001 to produce Collection 3. (Note that this first reprocessing was numbered Collection 3 rather than, as one would expect, Collec- tion 2.) Collection 3 was also the first version produced for the Aqua MODIS products. Collec- tion 4 reprocessing began in December 2002 and was terminated in December 2006. Production of the Collection 5 products commenced in mid-2006. Production of the "Tier-1" Collection 6 MODIS products, which includes the active fire products, commenced in February 2015 and will continue through 31 December 2021. Production of the MODIS product suite will at that point continue via the Collection 6.1 "mini-reprocessing" that was initiated for the land products in late 2020. 3.2 Level 2 Fire Products: MOD14 (Terra) and MYD14 (Aqua) This is the most basic fire product in which active fires and other thermal anomalies, such as volca- noes, are identified. The Level 2 product is defined in the MODIS orbit geometry covering an area of approximately 2340 x 2030 km in the along-scan and along-track directions, respectively. It is used to generate all of the higher-level fire products, and contains the', 'The objective is to provide the MODIS land products at consistent low resolution spa- tial and temporal scales suitable for global modeling. In practice, there is a fair amount of variation in the spatial and temporal gridding conventions used among the MODIS land CMG products. 3.1.4 Collections Reprocessing of the entire MODIS data archive is periodically performed to incorporate better cali- bration, algorithm refinements, and improved upstream data into all MODIS products. The updated MODIS data archive resulting from each reprocessing is referred to as a collection. Later collections supersede all earlier collections. For the Terra MODIS, Collection 1 consisted of the first products generated following launch. Terra MODIS data were reprocessed for the first time in June 2001 to produce Collection 3. (Note that this first reprocessing was numbered Collection 3 rather than, as one would expect, Collec- tion 2.) Collection 3 was also the first version produced for the Aqua MODIS products. Collec- tion 4 reprocessing began in December 2002 and was terminated in December 2006. Production of the Collection 5 products commenced in mid-2006. Production of the "Tier-1" Collection 6 MODIS products, which includes the active fire products, commenced in February 2015 and will continue through 31 December 2021. Production of the MODIS product suite will at that point continue via the Collection 6.1 "mini-reprocessing" that was initiated for the land products in late 2020. 3.2 Level 2 Fire Products: MOD14 (Terra) and MYD14 (Aqua) This is the most basic fire product in which active fires and other thermal anomalies, such as volca- noes, are identified. The Level 2 product is defined in the MODIS orbit geometry covering an area of approximately 2340 x 2030 km in the along-scan and along-track directions, respectively. It is used to generate all of the higher-level fire products, and contains the', 'The objective is to provide the MODIS land products at consistent low resolution spa- tial and temporal scales suitable for global modeling. In practice, there is a fair amount of variation in the spatial and temporal gridding conventions used among the MODIS land CMG products. 3.1.4 Collections Reprocessing of the entire MODIS data archive is periodically performed to incorporate better cali- bration, algorithm refinements, and improved upstream data into all MODIS products. The updated MODIS data archive resulting from each reprocessing is referred to as a collection. Later collections supersede all earlier collections. For the Terra MODIS, Collection 1 consisted of the first products generated following launch. Terra MODIS data were reprocessed for the first time in June 2001 to produce Collection 3. (Note that this first reprocessing was numbered Collection 3 rather than, as one would expect, Collec- tion 2.) Collection 3 was also the first version produced for the Aqua MODIS products. Collec- tion 4 reprocessing began in December 2002 and was terminated in December 2006. Production of the Collection 5 products commenced in mid-2006. Production of the "Tier-1" Collection 6 MODIS products, which includes the active fire products, commenced in February 2015 and will continue through 31 December 2021. Production of the MODIS product suite will at that point continue via the Collection 6.1 "mini-reprocessing" that was initiated for the land products in late 2020. 3.2 Level 2 Fire Products: MOD14 (Terra) and MYD14 (Aqua) This is the most basic fire product in which active fires and other thermal anomalies, such as volca- noes, are identified. The Level 2 product is defined in the MODIS orbit geometry covering an area of approximately 2340 x 2030 km in the along-scan and along-track directions, respectively. It is used to generate all of the higher-level fire products, and contains the', 'The objective is to provide the MODIS land products at consistent low resolution spa- tial and temporal scales suitable for global modeling. In practice, there is a fair amount of variation in the spatial and temporal gridding conventions used among the MODIS land CMG products. 3.1.4 Collections Reprocessing of the entire MODIS data archive is periodically performed to incorporate better cali- bration, algorithm refinements, and improved upstream data into all MODIS products. The updated MODIS data archive resulting from each reprocessing is referred to as a collection. Later collections supersede all earlier collections. For the Terra MODIS, Collection 1 consisted of the first products generated following launch. Terra MODIS data were reprocessed for the first time in June 2001 to produce Collection 3. (Note that this first reprocessing was numbered Collection 3 rather than, as one would expect, Collec- tion 2.) Collection 3 was also the first version produced for the Aqua MODIS products. Collec- tion 4 reprocessing began in December 2002 and was terminated in December 2006. Production of the Collection 5 products commenced in mid-2006. Production of the "Tier-1" Collection 6 MODIS products, which includes the active fire products, commenced in February 2015 and will continue through 31 December 2021. Production of the MODIS product suite will at that point continue via the Collection 6.1 "mini-reprocessing" that was initiated for the land products in late 2020. 3.2 Level 2 Fire Products: MOD14 (Terra) and MYD14 (Aqua) This is the most basic fire product in which active fires and other thermal anomalies, such as volca- noes, are identified. The Level 2 product is defined in the MODIS orbit geometry covering an area of approximately 2340 x 2030 km in the along-scan and along-track directions, respectively. It is used to generate all of the higher-level fire products, and contains the', 'The objective is to provide the MODIS land products at consistent low resolution spa- tial and temporal scales suitable for global modeling. In practice, there is a fair amount of variation in the spatial and temporal gridding conventions used among the MODIS land CMG products. 3.1.4 Collections Reprocessing of the entire MODIS data archive is periodically performed to incorporate better cali- bration, algorithm refinements, and improved upstream data into all MODIS products. The updated MODIS data archive resulting from each reprocessing is referred to as a collection. Later collections supersede all earlier collections. For the Terra MODIS, Collection 1 consisted of the first products generated following launch. Terra MODIS data were reprocessed for the first time in June 2001 to produce Collection 3. (Note that this first reprocessing was numbered Collection 3 rather than, as one would expect, Collec- tion 2.) Collection 3 was also the first version produced for the Aqua MODIS products. Collec- tion 4 reprocessing began in December 2002 and was terminated in December 2006. Production of the Collection 5 products commenced in mid-2006. Production of the "Tier-1" Collection 6 MODIS products, which includes the active fire products, commenced in February 2015 and will continue through 31 December 2021. Production of the MODIS product suite will at that point continue via the Collection 6.1 "mini-reprocessing" that was initiated for the land products in late 2020. 3.2 Level 2 Fire Products: MOD14 (Terra) and MYD14 (Aqua) This is the most basic fire product in which active fires and other thermal anomalies, such as volca- noes, are identified. The Level 2 product is defined in the MODIS orbit geometry covering an area of approximately 2340 x 2030 km in the along-scan and along-track directions, respectively. It is used to generate all of the higher-level fire products, and contains the', 'Harmonized Landsat Sentinel-2 (HLS) Product User Guide Product Version 2.0 J.G. Masek, J. Ju, M. Claverie, S. Skakun, J.-C. Roger, E. Vermote, B. Franch, Z. Yin, J. L. Dungan Principal Investigator: Dr. Jeffrey G. Masek, NASA/GSFC Correspondence email address: Jeffrey.G.Masek@nasa.gov 1 Acronyms AROP BRDF BT CMG ETM+ GDAL GLS HDF HLS KML MGRS MSI NBAR OLI QA RSR SDS SR SZA TM TOA UTM WRS Automated Registration and Orthorectification Package Bidirectional Reflectance Distribution Function Brightness temperature Climate Modelling Grid Enhanced Thematic Mapper Plus Geospatial Data Abstraction Library Global Land Survey Hierarchical Data Format Harmonized Landsat and Sentinel-2 Keyhole Markup Language Military Grid Reference System Multi-Spectral Instrument Nadir BRDF-normalized Reflectance Operational Land Imager Quality assessment Relative spectral response Scientific Data Sets Surface reflectance Sun zenith angle Thematic Mapper Top of atmosphere Universal Transverse Mercator Worldwide Reference System 2 1 Introduction The Harmonized Landsat and Sentinel-2 (HLS) project is a NASA initiative and collaboration with USGS to produce compatible surface reflectance (SR) data from a virtual constellation of satellite sensors, the Operational Land Imager (OLI) and Multi-Spectral Instrument (MSI) onboard the Landsat-8 and Sentinel-2 remote sensing satellites respectively. The combined measurement enables global land observation every 2-3 days at moderate (30 m) spatial resolution. The HLS project uses a set of algorithms to derive seamless products from OLI and MSI: atmospheric correction, cloud and cloud-shadow masking, spatial co-registration and common gridding, view angle normalization and spectral bandpass adjustment. The HLS data products can be regarded as the building blocks for a "data cube" so that a user may examine any pixel through time and treat the near-daily reflectance time series as though it came from a single sensor. The HLS suite contains two products, S30 and L30, derived from Sentinel-2 L1C and Landsat L1TP (Collection 2) input, respectively. They are gridded into', 'Input: Outputs: rdhdf5_aq, file, data1, prt=PRT is simply the Aquarius Level-2 file name and path. - IDL structure "data1" contains the full array of the different parameters in the level 2 data. - Output file "finfo.tags" contains a full listing of all the attributes & variables contained in different groups of the Level-2 file. read_aquarius_hdf_L3_mapped.pro Usage: Input: Outputs: rdhdf5_aq, file, data1, prt=PRT is simply the Aquarius Level-2 file name and path. - IDL structure "data1" contains the fully mapped 1 degree sea surface salinity data contained in the L3 file. - Output file "finfo.tags" contains a full listing of all the attributes & variables of the Level-3 file. 26 3 Aquarius Data Products Aquarius data archived at PO.DAAC include Level-0, Level-1A, Level-2, and Level-3 products. All files are in HDF5 format with the exception of the binary Level-0. The full suite of Aquarius data products (L0 through L3) are publicly available via the PO.DAAC, but only the L2 swath/orbital and L3 gridded/mapped are supported. Archived but unsupported products at PO.DAAC include L0, and L1A data. An overview of Aquarius dataset types is provided below, and a complete listing of archived products by level is given in table 2. A total of 177 L2 through L3 products are provided as part of the Aquarius V5.0 release. New Aquarius version releases such as V5.0 or V4.0, V3.0 and V2.0 before it typically only involve changes to L2 and L3 products, and not to the source L0 and L1A data. Users should also not that while both L0 and L1A products are available from the PO.DAAC only the L2 and L3 are actually supported. 3.1 Level-0 Product Level-0 files are raw binary data downloaded from the satellite. Typically, 4 files per day were produced during mission science operations (Phase E). These data were', 'Input: Outputs: rdhdf5_aq, file, data1, prt=PRT is simply the Aquarius Level-2 file name and path. - IDL structure "data1" contains the full array of the different parameters in the level 2 data. - Output file "finfo.tags" contains a full listing of all the attributes & variables contained in different groups of the Level-2 file. read_aquarius_hdf_L3_mapped.pro Usage: Input: Outputs: rdhdf5_aq, file, data1, prt=PRT is simply the Aquarius Level-2 file name and path. - IDL structure "data1" contains the fully mapped 1 degree sea surface salinity data contained in the L3 file. - Output file "finfo.tags" contains a full listing of all the attributes & variables of the Level-3 file. 26 3 Aquarius Data Products Aquarius data archived at PO.DAAC include Level-0, Level-1A, Level-2, and Level-3 products. All files are in HDF5 format with the exception of the binary Level-0. The full suite of Aquarius data products (L0 through L3) are publicly available via the PO.DAAC, but only the L2 swath/orbital and L3 gridded/mapped are supported. Archived but unsupported products at PO.DAAC include L0, and L1A data. An overview of Aquarius dataset types is provided below, and a complete listing of archived products by level is given in table 2. A total of 177 L2 through L3 products are provided as part of the Aquarius V5.0 release. New Aquarius version releases such as V5.0 or V4.0, V3.0 and V2.0 before it typically only involve changes to L2 and L3 products, and not to the source L0 and L1A data. Users should also not that while both L0 and L1A products are available from the PO.DAAC only the L2 and L3 are actually supported. 3.1 Level-0 Product Level-0 files are raw binary data downloaded from the satellite. Typically, 4 files per day were produced during mission science operations (Phase E). These data were']

    # results = []
    # for context in contexts:
    #     results.append(cmr_connector.reader(
    #             query=query,
    #             context=context,
    #         )
    #     )
    # print(results)
    # print(cmr_connector.evidence_select(query=query, reader_response_list=results))
    contexts = contexts[:2] + contexts[5:8]
    print(cmr_connector.multi_reader(query=query, contexts=contexts))
