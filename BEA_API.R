library(bea.R)

Key 	<- 'enter your key'

beaSearch('personal consumption', Key, asHtml = TRUE)

beaSearch('gross domestic', Key, asHtml = TRUE)

beaSpecs <- list(
  'UserID' = Key ,
  'Method' = 'GetData',
  'datasetname' = 'NIPA',
  'TableName' = 'T20305',
  'Frequency' = 'Q',
  'Year' = '2020',
  'ResultFormat' = 'json'
);

beaLong <- beaGet(beaSpecs, asWide = FALSE)
beaStatTab <- beaGet(beaSpecs, iTableStyle = FALSE)

beaPayload <- beaGet(beaSpecs);

beaViz(beaPayload)

View(beaSpecs)
