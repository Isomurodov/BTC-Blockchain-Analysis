# BTC Blockchain analysis
 Analyzes an individual BTC blocks with graphs
 
 
Overview

The following is the report of my analysis of the Bitcoin block 657354. It provides
information on statistical patterns of movements within this specific block. Such patterns
include the expected value of bitcoins moved in the block, the maximum and minimum
amounts of transactions, a few plots illustrating the distribution of transactions, and some
information regarding the fees paid by the users to consolidate their transactions in the
block.


Specifications

One of the important moments in the process of my analysis was the discovery of the
following: it is almost impossible to identify the owners of wallets. In other words, every
time one makes a transaction, he/she can generate new keys, which are all stored as a
collection in their bitcoin wallet. For this reason, my findings can offer only the information
about the movements/transactions between addresses, and not between wallets.


Parts of the code:

I divided my code into the following three parts:
   I. Retrieving the data
      I used this technique which was taught during the classes in order to get
      more complete data that would also include SegWit transactions as well as
      the missing addresses.
   II. Processing the data
       This is the part where actual analysis takes place. The following part includes
       one function (minmax), several variables, and a for loop comprising two
       other loops with if-else structures in each of them. After the execution of the
       loop, I display some data on the screen using the print function.
   III. Graphs
        In the last part, I used the pyplot method of the matplotlib library to
        represent the density plots and graphic visualizations of variables. In overall,
        there are six graphs. Three of them illustrate the distribution of transaction
        according to their size.
