<?php

/**
 * Schema object for: EstimateModRq
 * 
 * @author "Keith Palmer Jr." <Keith@ConsoliByte.com>
 * @license LICENSE.txt
 * 
 * @package QuickBooks
 * @subpackage QBXML
 */

/**
 * 
 */
require_once 'QuickBooks.php';

/**
 * 
 */
require_once 'QuickBooks/QBXML/Schema/Object.php';

/**
 * 
 */
class QuickBooks_QBXML_Schema_Object_EstimateModRq extends QuickBooks_QBXML_Schema_Object
{
	protected function &_qbxmlWrapper()
	{
		static $wrapper = 'EstimateMod';
		
		return $wrapper;
	}
	
	protected function &_dataTypePaths()
	{
		static $paths = array (
  'TxnID' => 'IDTYPE',
  'EditSequence' => 'STRTYPE',
  'CustomerRef ListID' => 'IDTYPE',
  'CustomerRef FullName' => 'STRTYPE',
  'ClassRef ListID' => 'IDTYPE',
  'ClassRef FullName' => 'STRTYPE',
  'TemplateRef ListID' => 'IDTYPE',
  'TemplateRef FullName' => 'STRTYPE',
  'TxnDate' => 'DATETYPE',
  'RefNumber' => 'STRTYPE',
  'BillAddress Addr1' => 'STRTYPE',
  'BillAddress Addr2' => 'STRTYPE',
  'BillAddress Addr3' => 'STRTYPE',
  'BillAddress Addr4' => 'STRTYPE',
  'BillAddress Addr5' => 'STRTYPE',
  'BillAddress City' => 'STRTYPE',
  'BillAddress State' => 'STRTYPE',
  'BillAddress PostalCode' => 'STRTYPE',
  'BillAddress Country' => 'STRTYPE',
  'BillAddress Note' => 'STRTYPE',
  'ShipAddress Addr1' => 'STRTYPE',			// This OSR says this is supported, but it's actually not... 
  'ShipAddress Addr2' => 'STRTYPE',
  'ShipAddress Addr3' => 'STRTYPE',
  'ShipAddress Addr4' => 'STRTYPE',
  'ShipAddress Addr5' => 'STRTYPE',
  'ShipAddress City' => 'STRTYPE',
  'ShipAddress State' => 'STRTYPE',
  'ShipAddress PostalCode' => 'STRTYPE',
  'ShipAddress Country' => 'STRTYPE',
  'ShipAddress Note' => 'STRTYPE',
  'IsActive' => 'BOOLTYPE',
  'CreateChangeOrder' => 'BOOLTYPE',
  'PONumber' => 'STRTYPE',
  'TermsRef ListID' => 'IDTYPE',
  'TermsRef FullName' => 'STRTYPE',
  'DueDate' => 'DATETYPE',
  'SalesRepRef ListID' => 'IDTYPE',
  'SalesRepRef FullName' => 'STRTYPE',
  'FOB' => 'STRTYPE',
  'ItemSalesTaxRef ListID' => 'IDTYPE',
  'ItemSalesTaxRef FullName' => 'STRTYPE',
  'Memo' => 'STRTYPE',
  'CustomerMsgRef ListID' => 'IDTYPE',
  'CustomerMsgRef FullName' => 'STRTYPE',
  'IsToBeEmailed' => 'BOOLTYPE',
  'IsTaxIncluded' => 'BOOLTYPE',
  'CustomerSalesTaxCodeRef ListID' => 'IDTYPE',
  'CustomerSalesTaxCodeRef FullName' => 'STRTYPE',
  'Other' => 'STRTYPE',
  'EstimateLineMod TxnLineID' => 'IDTYPE',
  'EstimateLineMod ItemRef ListID' => 'IDTYPE',
  'EstimateLineMod ItemRef FullName' => 'STRTYPE',
  'EstimateLineMod Desc' => 'STRTYPE',
  'EstimateLineMod Quantity' => 'QUANTYPE',
  'EstimateLineMod UnitOfMeasure' => 'STRTYPE',
  'EstimateLineMod OverrideUOMSetRef ListID' => 'IDTYPE',
  'EstimateLineMod OverrideUOMSetRef FullName' => 'STRTYPE',
  'EstimateLineMod Rate' => 'PRICETYPE',
  'EstimateLineMod RatePercent' => 'PERCENTTYPE',
  'EstimateLineMod ClassRef ListID' => 'IDTYPE',
  'EstimateLineMod ClassRef FullName' => 'STRTYPE',
  'EstimateLineMod Amount' => 'AMTTYPE',
  'EstimateLineMod InventorySiteRef ListID' => 'IDTYPE',
  'EstimateLineMod InventorySiteRef FullName' => 'STRTYPE',
  'EstimateLineMod SalesTaxCodeRef ListID' => 'IDTYPE',
  'EstimateLineMod SalesTaxCodeRef FullName' => 'STRTYPE',
  'EstimateLineMod MarkupRate' => 'PRICETYPE',
  'EstimateLineMod MarkupRatePercent' => 'PERCENTTYPE',
  'EstimateLineMod PriceLevelRef ListID' => 'IDTYPE',
  'EstimateLineMod PriceLevelRef FullName' => 'STRTYPE',
  'EstimateLineMod Other1' => 'STRTYPE',
  'EstimateLineMod Other2' => 'STRTYPE',
  'EstimateLineGroupMod TxnLineID' => 'IDTYPE',
  'EstimateLineGroupMod ItemGroupRef ListID' => 'IDTYPE',
  'EstimateLineGroupMod ItemGroupRef FullName' => 'STRTYPE',
  'EstimateLineGroupMod Quantity' => 'QUANTYPE',
  'EstimateLineGroupMod UnitOfMeasure' => 'STRTYPE',
  'EstimateLineGroupMod OverrideUOMSetRef ListID' => 'IDTYPE',
  'EstimateLineGroupMod OverrideUOMSetRef FullName' => 'STRTYPE',
  'EstimateLineGroupMod EstimateLineMod TxnLineID' => 'IDTYPE',
  'EstimateLineGroupMod EstimateLineMod ItemRef ListID' => 'IDTYPE',
  'EstimateLineGroupMod EstimateLineMod ItemRef FullName' => 'STRTYPE',
  'EstimateLineGroupMod EstimateLineMod Desc' => 'STRTYPE',
  'EstimateLineGroupMod EstimateLineMod Quantity' => 'QUANTYPE',
  'EstimateLineGroupMod EstimateLineMod UnitOfMeasure' => 'STRTYPE',
  'EstimateLineGroupMod EstimateLineMod OverrideUOMSetRef ListID' => 'IDTYPE',
  'EstimateLineGroupMod EstimateLineMod OverrideUOMSetRef FullName' => 'STRTYPE',
  'EstimateLineGroupMod EstimateLineMod Rate' => 'PRICETYPE',
  'EstimateLineGroupMod EstimateLineMod RatePercent' => 'PERCENTTYPE',
  'EstimateLineGroupMod EstimateLineMod ClassRef ListID' => 'IDTYPE',
  'EstimateLineGroupMod EstimateLineMod ClassRef FullName' => 'STRTYPE',
  'EstimateLineGroupMod EstimateLineMod Amount' => 'AMTTYPE',
  'EstimateLineGroupMod EstimateLineMod SalesTaxCodeRef ListID' => 'IDTYPE',
  'EstimateLineGroupMod EstimateLineMod SalesTaxCodeRef FullName' => 'STRTYPE',
  'EstimateLineGroupMod EstimateLineMod MarkupRate' => 'PRICETYPE',
  'EstimateLineGroupMod EstimateLineMod MarkupRatePercent' => 'PERCENTTYPE',
  'EstimateLineGroupMod EstimateLineMod PriceLevelRef ListID' => 'IDTYPE',
  'EstimateLineGroupMod EstimateLineMod PriceLevelRef FullName' => 'STRTYPE',
  'EstimateLineGroupMod EstimateLineMod Other1' => 'STRTYPE',
  'EstimateLineGroupMod EstimateLineMod Other2' => 'STRTYPE',
  'IncludeRetElement' => 'STRTYPE',
);
		
		return $paths;
	}
	
	protected function &_maxLengthPaths()
	{
		static $paths = array (
  'TxnID' => 0,
  'EditSequence' => 16,
  'CustomerRef ListID' => 0,
  'CustomerRef FullName' => 209,
  'ClassRef ListID' => 0,
  'ClassRef FullName' => 209,
  'TemplateRef ListID' => 0,
  'TemplateRef FullName' => 209,
  'TxnDate' => 0,
  'RefNumber' => 11,
  'BillAddress Addr1' => 41,
  'BillAddress Addr2' => 41,
  'BillAddress Addr3' => 41,
  'BillAddress Addr4' => 41,
  'BillAddress Addr5' => 41,
  'BillAddress City' => 31,
  'BillAddress State' => 21,
  'BillAddress PostalCode' => 13,
  'BillAddress Country' => 31,
  'BillAddress Note' => 41,
  'ShipAddress Addr1' => 41,
  'ShipAddress Addr2' => 41,
  'ShipAddress Addr3' => 41,
  'ShipAddress Addr4' => 41,
  'ShipAddress Addr5' => 41,
  'ShipAddress City' => 31,
  'ShipAddress State' => 21,
  'ShipAddress PostalCode' => 13,
  'ShipAddress Country' => 31,
  'ShipAddress Note' => 41,
  'IsActive' => 0,
  'CreateChangeOrder' => 0,
  'PONumber' => 25,
  'TermsRef ListID' => 0,
  'TermsRef FullName' => 209,
  'DueDate' => 0,
  'SalesRepRef ListID' => 0,
  'SalesRepRef FullName' => 209,
  'FOB' => 13,
  'ItemSalesTaxRef ListID' => 0,
  'ItemSalesTaxRef FullName' => 209,
  'Memo' => 4095,
  'CustomerMsgRef ListID' => 0,
  'CustomerMsgRef FullName' => 209,
  'IsToBeEmailed' => 0,
  'IsTaxIncluded' => 0,
  'CustomerSalesTaxCodeRef ListID' => 0,
  'CustomerSalesTaxCodeRef FullName' => 209,
  'Other' => 29,
  'EstimateLineMod TxnLineID' => 0,
  'EstimateLineMod ItemRef ListID' => 0,
  'EstimateLineMod ItemRef FullName' => 209,
  'EstimateLineMod Desc' => 4095,
  'EstimateLineMod Quantity' => 0,
  'EstimateLineMod UnitOfMeasure' => 31,
  'EstimateLineMod OverrideUOMSetRef ListID' => 0,
  'EstimateLineMod OverrideUOMSetRef FullName' => 209,
  'EstimateLineMod Rate' => 0,
  'EstimateLineMod RatePercent' => 0,
  'EstimateLineMod ClassRef ListID' => 0,
  'EstimateLineMod ClassRef FullName' => 209,
  'EstimateLineMod Amount' => 0,
  'EstimateLineMod InventorySiteRef ListID' => 0,
  'EstimateLineMod InventorySiteRef FullName' => 209,
  'EstimateLineMod SalesTaxCodeRef ListID' => 0,
  'EstimateLineMod SalesTaxCodeRef FullName' => 209,
  'EstimateLineMod MarkupRate' => 0,
  'EstimateLineMod MarkupRatePercent' => 0,
  'EstimateLineMod PriceLevelRef ListID' => 0,
  'EstimateLineMod PriceLevelRef FullName' => 209,
  'EstimateLineMod Other1' => 29,
  'EstimateLineMod Other2' => 29,
  'EstimateLineGroupMod TxnLineID' => 0,
  'EstimateLineGroupMod ItemGroupRef ListID' => 0,
  'EstimateLineGroupMod ItemGroupRef FullName' => 209,
  'EstimateLineGroupMod Quantity' => 0,
  'EstimateLineGroupMod UnitOfMeasure' => 31,
  'EstimateLineGroupMod OverrideUOMSetRef ListID' => 0,
  'EstimateLineGroupMod OverrideUOMSetRef FullName' => 209,
  'EstimateLineGroupMod EstimateLineMod TxnLineID' => 0,
  'EstimateLineGroupMod EstimateLineMod ItemRef ListID' => 0,
  'EstimateLineGroupMod EstimateLineMod ItemRef FullName' => 209,
  'EstimateLineGroupMod EstimateLineMod Desc' => 4095,
  'EstimateLineGroupMod EstimateLineMod Quantity' => 0,
  'EstimateLineGroupMod EstimateLineMod UnitOfMeasure' => 31,
  'EstimateLineGroupMod EstimateLineMod OverrideUOMSetRef ListID' => 0,
  'EstimateLineGroupMod EstimateLineMod OverrideUOMSetRef FullName' => 209,
  'EstimateLineGroupMod EstimateLineMod Rate' => 0,
  'EstimateLineGroupMod EstimateLineMod RatePercent' => 0,
  'EstimateLineGroupMod EstimateLineMod ClassRef ListID' => 0,
  'EstimateLineGroupMod EstimateLineMod ClassRef FullName' => 209,
  'EstimateLineGroupMod EstimateLineMod Amount' => 0,
  'EstimateLineGroupMod EstimateLineMod SalesTaxCodeRef ListID' => 0,
  'EstimateLineGroupMod EstimateLineMod SalesTaxCodeRef FullName' => 209,
  'EstimateLineGroupMod EstimateLineMod MarkupRate' => 0,
  'EstimateLineGroupMod EstimateLineMod MarkupRatePercent' => 0,
  'EstimateLineGroupMod EstimateLineMod PriceLevelRef ListID' => 0,
  'EstimateLineGroupMod EstimateLineMod PriceLevelRef FullName' => 209,
  'EstimateLineGroupMod EstimateLineMod Other1' => 29,
  'EstimateLineGroupMod EstimateLineMod Other2' => 29,
  'IncludeRetElement' => 50,
);
		
		return $paths;
	}
	
	protected function &_isOptionalPaths()
	{
		static $paths = array (
  'TxnID' => false,
  'EditSequence' => false,
  'CustomerRef ListID' => true,
  'CustomerRef FullName' => true,
  'ClassRef ListID' => true,
  'ClassRef FullName' => true,
  'TemplateRef ListID' => true,
  'TemplateRef FullName' => true,
  'TxnDate' => true,
  'RefNumber' => true,
  'BillAddress Addr1' => true,
  'BillAddress Addr2' => true,
  'BillAddress Addr3' => true,
  'BillAddress Addr4' => true,
  'BillAddress Addr5' => true,
  'BillAddress City' => true,
  'BillAddress State' => true,
  'BillAddress PostalCode' => true,
  'BillAddress Country' => true,
  'BillAddress Note' => true,
  'ShipAddress Addr1' => true,
  'ShipAddress Addr2' => true,
  'ShipAddress Addr3' => true,
  'ShipAddress Addr4' => true,
  'ShipAddress Addr5' => true,
  'ShipAddress City' => true,
  'ShipAddress State' => true,
  'ShipAddress PostalCode' => true,
  'ShipAddress Country' => true,
  'ShipAddress Note' => true,
  'IsActive' => true,
  'CreateChangeOrder' => true,
  'PONumber' => true,
  'TermsRef ListID' => true,
  'TermsRef FullName' => true,
  'DueDate' => true,
  'SalesRepRef ListID' => true,
  'SalesRepRef FullName' => true,
  'FOB' => true,
  'ItemSalesTaxRef ListID' => true,
  'ItemSalesTaxRef FullName' => true,
  'Memo' => true,
  'CustomerMsgRef ListID' => true,
  'CustomerMsgRef FullName' => true,
  'IsToBeEmailed' => true,
  'IsTaxIncluded' => true,
  'CustomerSalesTaxCodeRef ListID' => true,
  'CustomerSalesTaxCodeRef FullName' => true,
  'Other' => true,
  'EstimateLineMod TxnLineID' => false,
  'EstimateLineMod ItemRef ListID' => true,
  'EstimateLineMod ItemRef FullName' => true,
  'EstimateLineMod Desc' => true,
  'EstimateLineMod Quantity' => true,
  'EstimateLineMod UnitOfMeasure' => true,
  'EstimateLineMod OverrideUOMSetRef ListID' => true,
  'EstimateLineMod OverrideUOMSetRef FullName' => true,
  'EstimateLineMod Rate' => false,
  'EstimateLineMod RatePercent' => false,
  'EstimateLineMod ClassRef ListID' => true,
  'EstimateLineMod ClassRef FullName' => true,
  'EstimateLineMod Amount' => true,
  'EstimateLineMod InventorySiteRef ListID' => true,
  'EstimateLineMod InventorySiteRef FullName' => true,
  'EstimateLineMod SalesTaxCodeRef ListID' => true,
  'EstimateLineMod SalesTaxCodeRef FullName' => true,
  'EstimateLineMod MarkupRate' => false,
  'EstimateLineMod MarkupRatePercent' => false,
  'EstimateLineMod PriceLevelRef ListID' => true,
  'EstimateLineMod PriceLevelRef FullName' => true,
  'EstimateLineMod Other1' => true,
  'EstimateLineMod Other2' => true,
  'EstimateLineGroupMod TxnLineID' => false,
  'EstimateLineGroupMod ItemGroupRef ListID' => true,
  'EstimateLineGroupMod ItemGroupRef FullName' => true,
  'EstimateLineGroupMod Quantity' => true,
  'EstimateLineGroupMod UnitOfMeasure' => true,
  'EstimateLineGroupMod OverrideUOMSetRef ListID' => true,
  'EstimateLineGroupMod OverrideUOMSetRef FullName' => true,
  'EstimateLineGroupMod EstimateLineMod TxnLineID' => false,
  'EstimateLineGroupMod EstimateLineMod ItemRef ListID' => true,
  'EstimateLineGroupMod EstimateLineMod ItemRef FullName' => true,
  'EstimateLineGroupMod EstimateLineMod Desc' => true,
  'EstimateLineGroupMod EstimateLineMod Quantity' => true,
  'EstimateLineGroupMod EstimateLineMod UnitOfMeasure' => true,
  'EstimateLineGroupMod EstimateLineMod OverrideUOMSetRef ListID' => true,
  'EstimateLineGroupMod EstimateLineMod OverrideUOMSetRef FullName' => true,
  'EstimateLineGroupMod EstimateLineMod Rate' => false,
  'EstimateLineGroupMod EstimateLineMod RatePercent' => false,
  'EstimateLineGroupMod EstimateLineMod ClassRef ListID' => true,
  'EstimateLineGroupMod EstimateLineMod ClassRef FullName' => true,
  'EstimateLineGroupMod EstimateLineMod Amount' => true,
  'EstimateLineGroupMod EstimateLineMod SalesTaxCodeRef ListID' => true,
  'EstimateLineGroupMod EstimateLineMod SalesTaxCodeRef FullName' => true,
  'EstimateLineGroupMod EstimateLineMod MarkupRate' => false,
  'EstimateLineGroupMod EstimateLineMod MarkupRatePercent' => false,
  'EstimateLineGroupMod EstimateLineMod PriceLevelRef ListID' => true,
  'EstimateLineGroupMod EstimateLineMod PriceLevelRef FullName' => true,
  'EstimateLineGroupMod EstimateLineMod Other1' => true,
  'EstimateLineGroupMod EstimateLineMod Other2' => true,
  'IncludeRetElement' => true,
);
	}
	
	protected function &_sinceVersionPaths()
	{
		static $paths = array (
  'TxnID' => 999.99,
  'EditSequence' => 999.99,
  'CustomerRef ListID' => 999.99,
  'CustomerRef FullName' => 999.99,
  'ClassRef ListID' => 999.99,
  'ClassRef FullName' => 999.99,
  'TemplateRef ListID' => 999.99,
  'TemplateRef FullName' => 999.99,
  'TxnDate' => 999.99,
  'RefNumber' => 999.99,
  'BillAddress Addr1' => 999.99,
  'BillAddress Addr2' => 999.99,
  'BillAddress Addr3' => 999.99,
  'BillAddress Addr4' => 2,
  'BillAddress Addr5' => 6,
  'BillAddress City' => 999.99,
  'BillAddress State' => 999.99,
  'BillAddress PostalCode' => 999.99,
  'BillAddress Country' => 999.99,
  'BillAddress Note' => 6,
  'ShipAddress Addr1' => 999.99,
  'ShipAddress Addr2' => 999.99,
  'ShipAddress Addr3' => 999.99,
  'ShipAddress Addr4' => 2,
  'ShipAddress Addr5' => 6,
  'ShipAddress City' => 999.99,
  'ShipAddress State' => 999.99,
  'ShipAddress PostalCode' => 999.99,
  'ShipAddress Country' => 999.99,
  'ShipAddress Note' => 6,
  'IsActive' => 999.99,
  'CreateChangeOrder' => 999.99,
  'PONumber' => 999.99,
  'TermsRef ListID' => 999.99,
  'TermsRef FullName' => 999.99,
  'DueDate' => 999.99,
  'SalesRepRef ListID' => 999.99,
  'SalesRepRef FullName' => 999.99,
  'FOB' => 999.99,
  'ItemSalesTaxRef ListID' => 999.99,
  'ItemSalesTaxRef FullName' => 999.99,
  'Memo' => 999.99,
  'CustomerMsgRef ListID' => 999.99,
  'CustomerMsgRef FullName' => 999.99,
  'IsToBeEmailed' => 6,
  'IsTaxIncluded' => 6,
  'CustomerSalesTaxCodeRef ListID' => 999.99,
  'CustomerSalesTaxCodeRef FullName' => 999.99,
  'Other' => 6,
  'EstimateLineMod TxnLineID' => 999.99,
  'EstimateLineMod ItemRef ListID' => 999.99,
  'EstimateLineMod ItemRef FullName' => 999.99,
  'EstimateLineMod Desc' => 999.99,
  'EstimateLineMod Quantity' => 999.99,
  'EstimateLineMod UnitOfMeasure' => 7,
  'EstimateLineMod OverrideUOMSetRef ListID' => 999.99,
  'EstimateLineMod OverrideUOMSetRef FullName' => 999.99,
  'EstimateLineMod Rate' => 999.99,
  'EstimateLineMod RatePercent' => 999.99,
  'EstimateLineMod ClassRef ListID' => 999.99,
  'EstimateLineMod ClassRef FullName' => 999.99,
  'EstimateLineMod Amount' => 999.99,
  'EstimateLineMod InventorySiteRef ListID' => 999.99,
  'EstimateLineMod InventorySiteRef FullName' => 999.99,
  'EstimateLineMod SalesTaxCodeRef ListID' => 999.99,
  'EstimateLineMod SalesTaxCodeRef FullName' => 999.99,
  'EstimateLineMod MarkupRate' => 999.99,
  'EstimateLineMod MarkupRatePercent' => 999.99,
  'EstimateLineMod PriceLevelRef ListID' => 999.99,
  'EstimateLineMod PriceLevelRef FullName' => 999.99,
  'EstimateLineMod Other1' => 6,
  'EstimateLineMod Other2' => 6,
  'EstimateLineGroupMod TxnLineID' => 999.99,
  'EstimateLineGroupMod ItemGroupRef ListID' => 999.99,
  'EstimateLineGroupMod ItemGroupRef FullName' => 999.99,
  'EstimateLineGroupMod Quantity' => 999.99,
  'EstimateLineGroupMod UnitOfMeasure' => 7,
  'EstimateLineGroupMod OverrideUOMSetRef ListID' => 999.99,
  'EstimateLineGroupMod OverrideUOMSetRef FullName' => 999.99,
  'EstimateLineGroupMod EstimateLineMod TxnLineID' => 999.99,
  'EstimateLineGroupMod EstimateLineMod ItemRef ListID' => 999.99,
  'EstimateLineGroupMod EstimateLineMod ItemRef FullName' => 999.99,
  'EstimateLineGroupMod EstimateLineMod Desc' => 999.99,
  'EstimateLineGroupMod EstimateLineMod Quantity' => 999.99,
  'EstimateLineGroupMod EstimateLineMod UnitOfMeasure' => 7,
  'EstimateLineGroupMod EstimateLineMod OverrideUOMSetRef ListID' => 999.99,
  'EstimateLineGroupMod EstimateLineMod OverrideUOMSetRef FullName' => 999.99,
  'EstimateLineGroupMod EstimateLineMod Rate' => 999.99,
  'EstimateLineGroupMod EstimateLineMod RatePercent' => 999.99,
  'EstimateLineGroupMod EstimateLineMod ClassRef ListID' => 999.99,
  'EstimateLineGroupMod EstimateLineMod ClassRef FullName' => 999.99,
  'EstimateLineGroupMod EstimateLineMod Amount' => 999.99,
  'EstimateLineGroupMod EstimateLineMod SalesTaxCodeRef ListID' => 999.99,
  'EstimateLineGroupMod EstimateLineMod SalesTaxCodeRef FullName' => 999.99,
  'EstimateLineGroupMod EstimateLineMod MarkupRate' => 999.99,
  'EstimateLineGroupMod EstimateLineMod MarkupRatePercent' => 999.99,
  'EstimateLineGroupMod EstimateLineMod PriceLevelRef ListID' => 999.99,
  'EstimateLineGroupMod EstimateLineMod PriceLevelRef FullName' => 999.99,
  'EstimateLineGroupMod EstimateLineMod Other1' => 6,
  'EstimateLineGroupMod EstimateLineMod Other2' => 6,
  'IncludeRetElement' => 4,
);
		
		return $paths;
	}
	
	protected function &_isRepeatablePaths()
	{
		static $paths = array (
  'TxnID' => false,
  'EditSequence' => false,
  'CustomerRef ListID' => false,
  'CustomerRef FullName' => false,
  'ClassRef ListID' => false,
  'ClassRef FullName' => false,
  'TemplateRef ListID' => false,
  'TemplateRef FullName' => false,
  'TxnDate' => false,
  'RefNumber' => false,
  'BillAddress Addr1' => false,
  'BillAddress Addr2' => false,
  'BillAddress Addr3' => false,
  'BillAddress Addr4' => false,
  'BillAddress Addr5' => false,
  'BillAddress City' => false,
  'BillAddress State' => false,
  'BillAddress PostalCode' => false,
  'BillAddress Country' => false,
  'BillAddress Note' => false,
  'ShipAddress Addr1' => false,
  'ShipAddress Addr2' => false,
  'ShipAddress Addr3' => false,
  'ShipAddress Addr4' => false,
  'ShipAddress Addr5' => false,
  'ShipAddress City' => false,
  'ShipAddress State' => false,
  'ShipAddress PostalCode' => false,
  'ShipAddress Country' => false,
  'ShipAddress Note' => false,
  'IsActive' => false,
  'CreateChangeOrder' => false,
  'PONumber' => false,
  'TermsRef ListID' => false,
  'TermsRef FullName' => false,
  'DueDate' => false,
  'SalesRepRef ListID' => false,
  'SalesRepRef FullName' => false,
  'FOB' => false,
  'ItemSalesTaxRef ListID' => false,
  'ItemSalesTaxRef FullName' => false,
  'Memo' => false,
  'CustomerMsgRef ListID' => false,
  'CustomerMsgRef FullName' => false,
  'IsToBeEmailed' => false,
  'IsTaxIncluded' => false,
  'CustomerSalesTaxCodeRef ListID' => false,
  'CustomerSalesTaxCodeRef FullName' => false,
  'Other' => false,
  'EstimateLineMod TxnLineID' => false,
  'EstimateLineMod ItemRef ListID' => false,
  'EstimateLineMod ItemRef FullName' => false,
  'EstimateLineMod Desc' => false,
  'EstimateLineMod Quantity' => false,
  'EstimateLineMod UnitOfMeasure' => false,
  'EstimateLineMod OverrideUOMSetRef ListID' => false,
  'EstimateLineMod OverrideUOMSetRef FullName' => false,
  'EstimateLineMod Rate' => false,
  'EstimateLineMod RatePercent' => false,
  'EstimateLineMod ClassRef ListID' => false,
  'EstimateLineMod ClassRef FullName' => false,
  'EstimateLineMod Amount' => false,
  'EstimateLineMod InventorySiteRef ListID' => false,
  'EstimateLineMod InventorySiteRef FullName' => false,
  'EstimateLineMod SalesTaxCodeRef ListID' => false,
  'EstimateLineMod SalesTaxCodeRef FullName' => false,
  'EstimateLineMod MarkupRate' => false,
  'EstimateLineMod MarkupRatePercent' => false,
  'EstimateLineMod PriceLevelRef ListID' => false,
  'EstimateLineMod PriceLevelRef FullName' => false,
  'EstimateLineMod Other1' => false,
  'EstimateLineMod Other2' => false,
  'EstimateLineGroupMod TxnLineID' => false,
  'EstimateLineGroupMod ItemGroupRef ListID' => false,
  'EstimateLineGroupMod ItemGroupRef FullName' => false,
  'EstimateLineGroupMod Quantity' => false,
  'EstimateLineGroupMod UnitOfMeasure' => false,
  'EstimateLineGroupMod OverrideUOMSetRef ListID' => false,
  'EstimateLineGroupMod OverrideUOMSetRef FullName' => false,
  'EstimateLineGroupMod EstimateLineMod TxnLineID' => false,
  'EstimateLineGroupMod EstimateLineMod ItemRef ListID' => false,
  'EstimateLineGroupMod EstimateLineMod ItemRef FullName' => false,
  'EstimateLineGroupMod EstimateLineMod Desc' => false,
  'EstimateLineGroupMod EstimateLineMod Quantity' => false,
  'EstimateLineGroupMod EstimateLineMod UnitOfMeasure' => false,
  'EstimateLineGroupMod EstimateLineMod OverrideUOMSetRef ListID' => false,
  'EstimateLineGroupMod EstimateLineMod OverrideUOMSetRef FullName' => false,
  'EstimateLineGroupMod EstimateLineMod Rate' => false,
  'EstimateLineGroupMod EstimateLineMod RatePercent' => false,
  'EstimateLineGroupMod EstimateLineMod ClassRef ListID' => false,
  'EstimateLineGroupMod EstimateLineMod ClassRef FullName' => false,
  'EstimateLineGroupMod EstimateLineMod Amount' => false,
  'EstimateLineGroupMod EstimateLineMod SalesTaxCodeRef ListID' => false,
  'EstimateLineGroupMod EstimateLineMod SalesTaxCodeRef FullName' => false,
  'EstimateLineGroupMod EstimateLineMod MarkupRate' => false,
  'EstimateLineGroupMod EstimateLineMod MarkupRatePercent' => false,
  'EstimateLineGroupMod EstimateLineMod PriceLevelRef ListID' => false,
  'EstimateLineGroupMod EstimateLineMod PriceLevelRef FullName' => false,
  'EstimateLineGroupMod EstimateLineMod Other1' => false,
  'EstimateLineGroupMod EstimateLineMod Other2' => false,
  'IncludeRetElement' => true,
);
			
		return $paths;
	}
	
	/*
	abstract protected function &_inLocalePaths()
	{
		static $paths = array(
			'FirstName' => array( 'QBD', 'QBCA', 'QBUK', 'QBAU' ), 
			'LastName' => array( 'QBD', 'QBCA', 'QBUK', 'QBAU' ),
			);
		
		return $paths;
	}
	*/
	
	protected function &_reorderPathsPaths()
	{
		static $paths = array (
			'TxnID',
			'EditSequence',
			'CustomerRef ListID',
			'CustomerRef FullName',
			'ClassRef ListID',
			'ClassRef FullName',
			'TemplateRef ListID',
			'TemplateRef FullName',
			'TxnDate',
			'RefNumber',
			'BillAddress Addr1',
			'BillAddress Addr2',
			'BillAddress Addr3',
			'BillAddress Addr4',
			'BillAddress Addr5',
			'BillAddress City',
			'BillAddress State',
			'BillAddress PostalCode',
			'BillAddress Country',
			'BillAddress Note',
			'ShipAddress Addr1',
			'ShipAddress Addr2',
			'ShipAddress Addr3',
			'ShipAddress Addr4',
			'ShipAddress Addr5',
			'ShipAddress City',
			'ShipAddress State',
			'ShipAddress PostalCode',
			'ShipAddress Country',
			'ShipAddress Note',
			'IsActive',
			'CreateChangeOrder',
			'PONumber',
			'TermsRef ListID',
			'TermsRef FullName',
			'DueDate',
			'SalesRepRef ListID',
			'SalesRepRef FullName',
			'FOB',
			'ItemSalesTaxRef ListID',
			'ItemSalesTaxRef FullName',
			'Memo',
			'CustomerMsgRef ListID',
			'CustomerMsgRef FullName',
			'IsToBeEmailed',
			'IsTaxIncluded',
			'CustomerSalesTaxCodeRef ListID',
			'CustomerSalesTaxCodeRef FullName',
			'Other',
			'EstimateLineMod', 
			'EstimateLineMod TxnLineID',
			'EstimateLineMod ItemRef ListID',
			'EstimateLineMod ItemRef FullName',
			'EstimateLineMod Desc',
			'EstimateLineMod Quantity',
			'EstimateLineMod UnitOfMeasure',
			'EstimateLineMod OverrideUOMSetRef ListID',
			'EstimateLineMod OverrideUOMSetRef FullName',
			'EstimateLineMod Rate',
			'EstimateLineMod RatePercent',
			'EstimateLineMod ClassRef ListID',
			'EstimateLineMod ClassRef FullName',
			'EstimateLineMod Amount',
			'EstimateLineMod InventorySiteRef ListID',
			'EstimateLineMod InventorySiteRef FullName',
			'EstimateLineMod SalesTaxCodeRef ListID',
			'EstimateLineMod SalesTaxCodeRef FullName',
			'EstimateLineMod MarkupRate',
			'EstimateLineMod MarkupRatePercent',
			'EstimateLineMod PriceLevelRef ListID',
			'EstimateLineMod PriceLevelRef FullName',
			'EstimateLineMod Other1',
			'EstimateLineMod Other2',
			'EstimateLineGroupMod', 
			'EstimateLineGroupMod TxnLineID',
			'EstimateLineGroupMod ItemGroupRef ListID',
			'EstimateLineGroupMod ItemGroupRef FullName',
			'EstimateLineGroupMod Quantity',
			'EstimateLineGroupMod UnitOfMeasure',
			'EstimateLineGroupMod OverrideUOMSetRef ListID',
			'EstimateLineGroupMod OverrideUOMSetRef FullName',
			'EstimateLineGroupMod EstimateLineMod TxnLineID',
			'EstimateLineGroupMod EstimateLineMod ItemRef ListID',
			'EstimateLineGroupMod EstimateLineMod ItemRef FullName',
			'EstimateLineGroupMod EstimateLineMod Desc',
			'EstimateLineGroupMod EstimateLineMod Quantity',
			'EstimateLineGroupMod EstimateLineMod UnitOfMeasure',
			'EstimateLineGroupMod EstimateLineMod OverrideUOMSetRef ListID',
			'EstimateLineGroupMod EstimateLineMod OverrideUOMSetRef FullName',
			'EstimateLineGroupMod EstimateLineMod Rate',
			'EstimateLineGroupMod EstimateLineMod RatePercent',
			'EstimateLineGroupMod EstimateLineMod ClassRef ListID',
			'EstimateLineGroupMod EstimateLineMod ClassRef FullName',
			'EstimateLineGroupMod EstimateLineMod Amount',
			'EstimateLineGroupMod EstimateLineMod SalesTaxCodeRef ListID',
			'EstimateLineGroupMod EstimateLineMod SalesTaxCodeRef FullName',
			'EstimateLineGroupMod EstimateLineMod MarkupRate',
			'EstimateLineGroupMod EstimateLineMod MarkupRatePercent',
			'EstimateLineGroupMod EstimateLineMod PriceLevelRef ListID',
			'EstimateLineGroupMod EstimateLineMod PriceLevelRef FullName',
			'EstimateLineGroupMod EstimateLineMod Other1',
			'EstimateLineGroupMod EstimateLineMod Other2',
			'IncludeRetElement',
		);
		
		return $paths;
	}
}
