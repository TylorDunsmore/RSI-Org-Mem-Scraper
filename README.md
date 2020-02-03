# RSI-Org-Mem-Scraper
Organization and member scraper for Roberts Space Industries (Star Citizen)

Script is designed to pull the organizations in order from largest to smallest.
Once the organization list is completed the members are then pulled from the listed organizations.

Standard variables to be changed are as follows:

input_start_page = 1      
input_max_org_pages = 20  
input_min_org_size = 100

Standard output are two .csv files.

First is the organization file.
Example output:

  NAME	                              INITIALS	    SIZE
  
  Test Squadron - Best Squardon!	    TEST	        18985

Second is the member file.
Example output:

  NAME	              HANDLE	        RANK	        ORG	          AFFILIATION
  
  Burgalash	          Burgalash	      Cadet	        TEST	        1
  
Based on the standard variables the run time is approximately 2 hours with ~395 organizations and ~185,000 members.
