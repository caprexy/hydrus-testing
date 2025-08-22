import json

from hydrus.core import HydrusConstants as HC
from hydrus.core import HydrusData
from hydrus.core import HydrusExceptions
from hydrus.core import HydrusGlobals as HG
from hydrus.core import HydrusSerialisable

from hydrus.core.networking import HydrusServerRequest

from hydrus.client import ClientConstants as CC
from hydrus.client import ClientGlobals as CG
from hydrus.client.networking.api import ClientLocalServerResources
from hydrus.client.networking.api import ClientLocalServerCore
from hydrus.core.networking import HydrusServerRequest
from hydrus.core.networking import HydrusServerResources

class APISubscriptionsGetSubscriptionsResource( ClientLocalServerResources.HydrusResourceClientAPIRestricted ):
    
    def __init__(self, service, domain):
        ClientLocalServerResources.HydrusResourceClientAPIRestricted.__init__(self, service, domain)
    
    def _CheckAPIPermissions( self, request ):
        request.client_api_permissions.CheckPermission( HC.CLIENT_API_PERMISSION_SEARCH_FILES )
    
    def _reportDataUsed( self, request, bytes_used ):
        return request.client_api_permissions.ReportDataUsed( bytes_used )
    
    def _reportRequestUsed( self, request ):
        return request.client_api_permissions.ReportRequestUsed()
    
    def _threadDoGETJob( self, request: HydrusServerRequest.HydrusRequest ):
        subscriptions = CG.client_controller.subscriptions_manager.GetSubscriptions()
        
        subs_info = []
        
        for subscription in subscriptions:
            query_headers = subscription.GetQueryHeaders()
            queries_info = []
            
            for query_header in query_headers:
                query_info = {
                    'query_text': query_header.GetQueryText(),
                    'human_name': query_header.GetHumanName(),
                    'display_name': query_header.GetDisplayName(),
                    'last_check_time': query_header.GetLastCheckTime(),
                    'next_check_time': query_header.GetNextCheckTime(),
                    'next_check_status': query_header.GetNextCheckStatusString(),
                    'paused': query_header.IsPaused(),
                    'dead': query_header.IsDead(),
                    'checking_now': query_header.IsCheckingNow(),
                    'can_check_now': query_header.CanCheckNow(),
                    'checker_status': query_header.GetCheckerStatus(),
                    'file_velocity': query_header.GetFileVelocityInfo(),
                    'file_seed_cache_status': query_header.GetFileSeedCacheStatus().GetStatusText(),
                    'last_file_time': query_header.GetLatestAddedTime()
                }
                queries_info.append(query_info)
            
            sub_dict = {
                'name': subscription.GetName(),
                'gug_name': subscription.GetGUGKeyAndName()[1],
                'queries': queries_info
            }
            subs_info.append(sub_dict)
        
        api_info_dict = {"subscriptions": subs_info}
        
        body = ClientLocalServerCore.Dumps( api_info_dict, request.preferred_mime )
        
        response_context = HydrusServerResources.ResponseContext( 200, mime = request.preferred_mime, body = body )
        
        return response_context
