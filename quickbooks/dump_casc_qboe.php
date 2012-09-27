<?php

/**
 * Dumping data from QuickBooks Online Edition
 * 
 * * IMPORTANT * 
 * Before using this file, you must go through the Intuit application 
 * registration process. This is documented here: 
 * 	http://wiki.consolibyte.com/wiki/doku.php/quickbooks_online_edition
 * 
 * @enhanced by Josephson
 */

// 
header('Content-Type: text/plain');

// 28Aug2012 - Josephson (DIRECTORY_SEPARATOR shorter variable name!)
$ds = DIRECTORY_SEPARATOR;
// 
ini_set('include_path', ini_get('include_path') . PATH_SEPARATOR . dirname(__FILE__) . $ds . '..'. $ds . 'QuickBooks');

var_dump(ini_get('include_path'));
#die("Wait wait wait!\n");

error_reporting(E_ALL | E_STRICT);

/**
 * Require the QuickBooks base classes
 */
require_once '../QuickBooks.php';

// Tell the framework what username to use to keep track of your requests
//	(You can just make these up at the moment, they don't do anything...)
$username = 'api';
$password = 'password';

// Tell the QuickBooks_API class you'll be connecting to QuickBooks Online Edition
$source_type = QuickBooks_API::SOURCE_ONLINE_EDITION;

// If you want to log requests/responses to a database, you can provide a DSN-
//	style connection string to the database here. 
$api_driver_dsn = null;
// $api_driver_dsn = 'mysql://root:@localhost/quickbooks_api';
// $api_driver_dsn = 'pgsql://pgsql@localhost/quickbooks_onlineedition';

// This is not applicable to QBOE
$source_dsn = null;

// Various API options
$api_options = array();

// Options for QBOE
$source_options = array(
	// There are two models of communication for QuickBooks Online Edition. One 
	//	is the 'Hosted' model, the other is the 'Desktop' model. You can use 
	//	either if you're developing a web application. 
	// 
	// If you're using the 'Desktop' model of communication with QuickBooks OE, 
	//	then you can safely ignore the 'certificate' parameter. The 'Desktop' 
	//	model of communication with QBOE is easier to set up, at the expense of 
	//	being a little less secure. 
	// 
	//	
	// These next 3 configuration options are *required* 
	//	You should have been supplied with all 3 of these values when you went 
	//	through the Application Registration process on the Intuit Developer 
	//	website. 
	//	
	//	connection_ticket - QuickBooks Online Edition does an HTTP POST to your callback URL to send you this
	//	application_login - Provided by the application registration page
	//	application_id - Provided by the application registration page 	
	
#	'connection_ticket' => 'TGT-211-rQErMOrlyR$vdN7dVHQnNA', 
#	'application_login' => 'saas.consolibyte.com', 
#	'application_id' => '178965328', 
	'connection_ticket' => 'TGT-208-RC8fupn3ufHCfI7s2zHFEA', 
	'application_login' => 'spof-quickbooks-dump.cascadeo.com', 
	'application_id' => '514135205', 
	
	// This is just for debugging/testing, and you should comment this out... 
	//'override_session_ticket' => 'V1-184-uVBpWbpD17931L2hMNMw$A:134864687', 	// Comment this line out unless you know what you're doing!
	);

// Driver options
$driver_options = array();

// If you want to log requests/responses to a database, initialize the database
if ($api_driver_dsn and !QuickBooks_Utilities::initialized($api_driver_dsn))
{
	QuickBooks_Utilities::initialize($api_driver_dsn);
	QuickBooks_Utilities::createUser($api_driver_dsn, $username, $password);
}

// Create the API instance
$API = new QuickBooks_API($api_driver_dsn, $username, $source_type, $source_dsn, $api_options, $source_options, $driver_options);

// Turn on debugging mode
// 28Aug2012 - Josephson (turn it off for the meantime)
$API->useDebugMode(false);

// With QuickBooks Online Edition, the API can return values to you rather than 
//	using callback functions to return values. Remember that is you use this, 
//	your code will be less portable to systems using non-real-time connections
	//	(i.e. the QuickBooks Web Connector). 
//$API->enableRealtime(true);

// Let's get some general information about this connection to QBOE:
print('Our connection ticket is: ' . $API->connectionTicket() . "\n");
print('Our session ticket is: ' . $API->sessionTicket() . "\n");
print('Our application id is: ' . $API->applicationID() . "\n");
print('Our application login is: ' . $API->applicationLogin() . "\n");
print("\n"); 
print('Last error number: ' . $API->errorNumber() . "\n");
print('Last error message: ' . $API->errorMessage() . "\n");
print("\n");


// The "raw" approach to accessing QuickBooks Online Edition is to build and 
//	parse the qbXML requests/responses send to/from QuickBooks yourself. Here 
//	is an example of querying for a customer by building a raw qbXML request. 
//	The qbXML response is passed back to you in the _raw_qbxml_callback() 
//	function as the $qbxml parameter. 


#$return = $API->qbxml('
#		<InvoiceQueryRq>
#			<RefNumber>5381</RefNumber>
#		</InvoiceQueryRq>', '_raw_qbxml_callback');
#$return = $API->qbxml('
#		<InvoiceQueryRq>
#		</InvoiceQueryRq>', '_raw_qbxml_callback');

// This function gets called when QuickBooks Online Edition sends a response back
// 28Aug2012 - Josephson ($err instead of &$err)
function _raw_qbxml_callback($method, $action, $ID, $err, $qbxml, $Iterator, $qbres)
{
	print('We got back this qbXML from QuickBooks Online Edition: ' . $qbxml);
	if ($err != '') {
		var_dump($err);
		die("Unsuccessful.. please try again...\n");
	}
}

// 29Aug2012 - Josephson (save journal entries - TEST; and other data that can be exported/dumped)
$OBJECT_SAVED = 'Journal_Entries';
$API->qbxml('<JournalEntryQueryRq></JournalEntryQueryRq>', '_write_to_file');
$OBJECT_SAVED = 'Receive_Payments';
$API->qbxml('<ReceivePaymentQueryRq></ReceivePaymentQueryRq>', '_write_to_file');
$OBJECT_SAVED = 'Accounts';
$API->qbxml('<AccountQueryRq></AccountQueryRq>', '_write_to_file');
// ItemQueryRq
$OBJECT_SAVED = 'Item'; // Yes, 'Querys'! To possibly avoid some kind of 'importing' problem in the future!
$API->qbxml(
'<ItemQueryRq>
</ItemQueryRq>', '_write_to_file');
// Credit Card Charge
$OBJECT_SAVED = 'Credit_Card_Charges';
$API->qbxml(
'<CreditCardChargeQueryRq>
</CreditCardChargeQueryRq>', '_write_to_file');


// 29Aug2012 - Josephson

// For QuickBooks Online Edition, you can use real-time connections so that you 
//	get return values instead of having to write callback functions. Note that 
//	if you do this, you make your code less portable to other editions of 
//	QuickBooks that do not support real-time connections (i.e. QuickBooks 
//	desktop editions via the Web Connector)
if ($API->usingRealtime())
{
	print('Our real-time response from QuickBooks Online Edition was: ');
	print_r($return);
}

// 28Aug2012 - Josephson
// exit;

// 28Aug2012 - Josephson

// Here's a demo of querying for customers with a specific name: 
$name = 'MR JUAN DEY-LA CRUWZ MD';
// Here's how to fetch that customer by name
#$API->getCustomerByName($name, '_get_customer_callback', 15);

// 28Aug2012 - Josephson (set object being backed up - i.e. Customer, Vendor, etc...)
#$OBJECT_SAVED = 'Customers';
#$API->searchCustomers(array(), '_write_to_file');;
$OBJECT_SAVED = 'Vendors';
$API->searchVendors(array(), '_write_to_file');;

// 28Aug2012 - Josephson ($err instead of &$err)
function _get_customer_callback($method, $action, $ID, $err, $qbxml, $Iterator, $qbres)
{
	print('This is customer #' . $ID . ' we fetched: ' . "\n");
	// 28Aug2012 - Josephson
	// print_r($Iterator);
	var_dump($Iterator);
	var_dump($qbxml);
	print("\n");
}

// 28Aug2012 - Josephson
function _write_to_file($method, $action, $ID, $err, $qbxml, $Iterator, $qbres) {
	global $ds, $OBJECT_SAVED;
	$outfile_name = DIRNAME(__FILE__) . "{$ds}outfile_{$OBJECT_SAVED}_" . date("Y-m-d_His") . ".txt";
	$outfile = fopen($outfile_name, 'w');
	fwrite($outfile, $qbxml . "\n");
	fclose($outfile);
	print("Results saved to {$outfile_name}\n");
}


// 29Aug2012 - Josephson
// trying to get Employees' data
$employees = null;
$OBJECT_SAVED = 'Employees';

$empObj = new QuickBooks_Object_Employee();
$empErr = '';
// holder of callback function to include
$wrkCallback = '_write_to_file';

$API->doQueryInBehalf(__METHOD__, QUICKBOOKS_QUERY_EMPLOYEE, QUICKBOOKS_OBJECT_EMPLOYEE, $empObj, $wrkCallback, $source_options['application_id'], null, $empErr, null);

// INVOICE
$OBJECT_SAVED = 'Invoices';
// holder of what kind of object/s will be saved
$wrkObj = new QuickBooks_Object_Invoice();
// holder of any error message
$wrkErr = '';
$API->doQueryInBehalf(__METHOD__, QUICKBOOKS_QUERY_INVOICE, QUICKBOOKS_OBJECT_INVOICE, $wrkObj, $wrkCallback, $source_options['application_id'], null, $empErr, null);

// 30Aug2012 - Josephson (DEPOSIT)
$OBJECT_SAVED = 'Deposits';
$wrkObj = new QuickBooks_Object_Deposit();
$wrkErr = '';
#$API->doQueryInBehalf(__METHOD__, QUICKBOOKS_QUERY_DEPOSIT, QUICKBOOKS_OBJECT_DEPOSIT, $wrkObj, $wrkCallback, $source_options['application_id'], null, $empErr, null);
// 03Sept2012 - Josephson (BillQueryRq)
$API->qbxml(
'<DepositAddRq>
</DepositAddRq>', '_raw_qbxml_callback');


// 29Aug2012 - Josephson

die('wait!\n');
// 28Aug2012 - Josephson

