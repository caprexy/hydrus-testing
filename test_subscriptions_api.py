import unittest
import time
from unittest.mock import MagicMock, patch

from hydrus.core import HydrusData
from hydrus.core import HydrusGlobals as HG
from hydrus.core import HydrusConstants as HC

from hydrus.client import ClientConstants as CC
from hydrus.client import ClientGlobals as CG
from hydrus.client.importing import ClientImportSubscriptions
from hydrus.client.importing import ClientImportSubscriptionQuery
from hydrus.client.networking.api import ClientLocalServerResourcesSubscriptions

class TestSubscriptionsAPI( unittest.TestCase ):
    
    def setUp( self ):
        self.subscription = ClientImportSubscriptions.Subscription( "test_sub" )
        
        # Mock the query header
        self.query_header = MagicMock( spec=ClientImportSubscriptionQuery.SubscriptionQueryHeader )
        self.query_header.GetQueryLogContainerName.return_value = "test_container"
        
        self.subscription._query_headers = [ self.query_header ]
        
        # Mock the query log container
        self.query_log_container = MagicMock()
        self.file_seed_cache = MagicMock()
        self.query_log_container.GetFileSeedCache.return_value = self.file_seed_cache
        
        # Mock the client controller read
        CG.client_controller = MagicMock()
        CG.client_controller.Read.return_value = self.query_log_container
        
    def test_get_last_downloaded_file_time( self ):
        # Setup
        file_seed = MagicMock()
        file_seed.status = CC.STATUS_SUCCESSFUL_AND_NEW
        file_seed.created = 1234567890
        
        self.file_seed_cache.GetFirstFileSeed.return_value = file_seed
        
        # Test
        result = self.subscription.GetLastDownloadedFileTime()
        
        # Verify
        self.assertEqual( result, 1234567890 )
        
    def test_get_last_checked_time( self ):
        # Setup
        self.query_log_container.GetLastCheckedTime.return_value = 1234567890
        
        # Test
        result = self.subscription.GetLastCheckedTime()
        
        # Verify
        self.assertEqual( result, 1234567890 )
        
    def test_get_next_check_time( self ):
        # Setup
        self.query_log_container.GetNextCheckTime.return_value = 1234567890
        
        # Test
        result = self.subscription.GetNextCheckTime()
        
        # Verify
        self.assertEqual( result, 1234567890 )
        
    def test_get_status_paused( self ):
        # Setup
        self.subscription._paused = True
        
        # Test
        result = self.subscription.GetStatus()
        
        # Verify
        self.assertEqual( result, "paused" )
        
    def test_get_status_delayed( self ):
        # Setup
        self.subscription._paused = False
        self.subscription._no_work_until = time.time() + 3600  # 1 hour from now
        self.subscription._no_work_until_reason = "test delay"
        
        # Test
        result = self.subscription.GetStatus()
        
        # Verify
        self.assertEqual( result, "delayed: test delay" )
        
    def test_get_status_active( self ):
        # Setup
        self.subscription._paused = False
        self.subscription._no_work_until = 0
        
        # Test
        result = self.subscription.GetStatus()
        
        # Verify
        self.assertEqual( result, "active" )

if __name__ == '__main__':
    unittest.main()
