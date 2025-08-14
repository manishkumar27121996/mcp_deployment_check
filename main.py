
# import streamlit as st
# import requests
# import json
# import uuid
# import pandas as pd
# from datetime import datetime
# import time

# # Configure Streamlit page
# st.set_page_config(
#     page_title="Summary Agent",
#     page_icon="🤖",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # API Configuration
# API_BASE_URL = "https://mcp-summarization.minervaiotstaging.com"
# CHAT_ENDPOINT = f"{API_BASE_URL}/chat"
# HEALTH_ENDPOINT = f"{API_BASE_URL}/health"
# HIERARCHY_ENDPOINT = f"{API_BASE_URL}/hierarchy/access"

# def check_api_health():
#     """Check if the API is running and healthy"""
#     try:
#         response = requests.get(HEALTH_ENDPOINT, timeout=5)
#         if response.status_code == 200:
#             return True, response.json()
#         else:
#             return False, f"API returned status code: {response.status_code}"
#     except requests.exceptions.RequestException as e:
#         return False, f"Connection error: {str(e)}"

# def get_user_hierarchy_info(bearer_token, refresh_cache=False):
#     """Get user hierarchy information from the API"""
#     try:
#         headers = {"Authorization": f"Bearer {bearer_token}"}
#         params = {"refresh_cache": refresh_cache} if refresh_cache else {}
        
#         response = requests.get(
#             HIERARCHY_ENDPOINT, 
#             headers=headers, 
#             params=params,
#             timeout=10
#         )
        
#         if response.status_code == 200:
#             return True, response.json()
#         else:
#             return False, f"Error: {response.status_code} - {response.text}"
#     except requests.exceptions.RequestException as e:
#         return False, f"Connection error: {str(e)}"

# def send_chat_message(message, bearer_token, session_id):
#     """Send a chat message to the API"""
#     try:
#         headers = {
#             "Authorization": f"Bearer {bearer_token}",
#             "Content-Type": "application/json"
#         }
        
#         payload = {
#             "message": message,
#             "session_id": session_id
#         }
        
#         response = requests.post(
#             CHAT_ENDPOINT, 
#             headers=headers, 
#             json=payload, 
#             timeout=120  # Increased timeout for complex queries
#         )
        
#         if response.status_code == 200:
#             return True, response.json()
#         else:
#             return False, f"Error {response.status_code}: {response.text}"
            
#     except requests.exceptions.RequestException as e:
#         return False, f"Connection error: {str(e)}"

# def main():
#     # Header
#     st.title("🤖 Summary Agent")
#     st.markdown("**Enhanced AI Assistant with Hierarchical Access Control**")
    
#     # Sidebar for configuration
#     with st.sidebar:
#         st.header("🔧 Configuration")
        
#         # API Health Check
#         st.subheader("🏥 API Status")
#         health_status, health_data = check_api_health()
        
#         if health_status:
#             if isinstance(health_data, dict):
#                 api_status = health_data.get("status", "unknown")
#                 tunnel_active = health_data.get("tunnel_active", False)
                
#                 # Show status with appropriate color
#                 if api_status == "healthy":
#                     st.success("✅ API is healthy")
#                 elif api_status == "degraded":
#                     if not tunnel_active:
#                         st.warning("⚠️ API running (SSH tunnel inactive)")
#                         st.info("💡 SSH tunnel may connect automatically when needed")
#                     else:
#                         st.warning("⚠️ API status degraded")
#                 else:
#                     st.info(f"ℹ️ API status: {api_status}")
                
#                 # Show key components status
#                 components = health_data.get("components", {})
#                 col1, col2 = st.columns(2)
                
#                 with col1:
#                     fastapi_status = components.get("fastapi", "unknown")
#                     if fastapi_status == "running":
#                         st.success("🚀 FastAPI: Running")
#                     else:
#                         st.error(f"❌ FastAPI: {fastapi_status}")
                
#                 with col2:
#                     tunnel_status = "Active" if tunnel_active else "Inactive"
#                     tunnel_color = st.success if tunnel_active else st.info
#                     tunnel_color(f"🔗 SSH: {tunnel_status}")
                
#                 # Production Safety Status
#                 production_safety = health_data.get("production_safety", {})
#                 with st.expander("🛡️ Production Safety"):
#                     st.write("**Smart Limit System:**", production_safety.get("smart_limit_system", "unknown"))
#                     st.write("**Hierarchy Control:**", production_safety.get("team_lead_manager_hierarchy", "unknown"))
#                     st.write("**Date Range Limit:**", production_safety.get("date_range_limit", "unknown"))
#                     st.write("**Cost Control:**", production_safety.get("cost_control", "unknown"))
                
#                 # Pipeline Status
#                 pipeline_status = health_data.get("pipeline_status", {})
#                 with st.expander("⚙️ Pipeline Status"):
#                     for phase, status in pipeline_status.items():
#                         phase_name = phase.replace("_", " ").title()
#                         st.write(f"**{phase_name}:** {status}")
                
#                 # Agent Statistics
#                 agents = components.get("agents", {})
#                 if any(agents.values()):
#                     with st.expander("🤖 Active Agents"):
#                         st.write(f"**Verification Agents:** {agents.get('verification_agents', 0)}")
#                         st.write(f"**Data Agents:** {agents.get('data_agents', 0)}")
#                         st.write(f"**MCP Tools:** {agents.get('mcp_tools_instances', 0)}")
#                 else:
#                     st.info("🤖 No active agent sessions")
                
#                 # Raw data for debugging (collapsed by default)
#                 with st.expander("🔧 Raw API Response (Debug)"):
#                     st.json(health_data)
#             else:
#                 st.success("✅ API is accessible")
#         else:
#             st.error(f"❌ API is not accessible")
#             st.error(health_data)
#             st.stop()
        
#         # Authentication
#         st.subheader("🔐 Authentication")
#         bearer_token = st.text_input(
#             "Bearer Token",
#             type="password",
#             help="Enter your JWT bearer token for API access"
#         )
        
#         if not bearer_token:
#             st.warning("⚠️ Please enter your bearer token to continue")
#             st.stop()
        
#         # Session Management
#         st.subheader("📝 Session")
#         if "session_id" not in st.session_state:
#             st.session_state.session_id = str(uuid.uuid4())
        
#         st.text(f"Session ID: {st.session_state.session_id[:8]}...")
        
#         if st.button("🔄 New Session"):
#             st.session_state.session_id = str(uuid.uuid4())
#             st.session_state.messages = []
#             # Clear hierarchy cache when starting new session
#             if "hierarchy_data_cache" in st.session_state:
#                 del st.session_state["hierarchy_data_cache"]
#             st.rerun()
        
#         # User Hierarchy Information
#         st.subheader("👤 User Access")
        
#         # Add refresh button
#         col1, col2 = st.columns([3, 1])
#         with col1:
#             st.write("**Hierarchy Information**")
#         with col2:
#             refresh_clicked = st.button("🔄 Refresh", help="Refresh hierarchy data from database")
        
#         # Get hierarchy info (with refresh if button was clicked)
#         if refresh_clicked:
#             with st.spinner("🔄 Refreshing hierarchy data..."):
#                 hierarchy_success, hierarchy_data = get_user_hierarchy_info(bearer_token, refresh_cache=True)
#                 # Clear any cached data
#                 if "hierarchy_data_cache" in st.session_state:
#                     del st.session_state["hierarchy_data_cache"]
#                 # Cache the fresh data
#                 st.session_state["hierarchy_data_cache"] = (hierarchy_success, hierarchy_data)
                
#                 if hierarchy_success:
#                     st.success("✅ Hierarchy data refreshed successfully!")
#                 else:
#                     st.error("❌ Failed to refresh hierarchy data")
#         else:
#             # Use cached data if available, otherwise fetch fresh
#             if "hierarchy_data_cache" in st.session_state:
#                 hierarchy_success, hierarchy_data = st.session_state["hierarchy_data_cache"]
#                 st.info("📦 Using cached hierarchy data")
#             else:
#                 with st.spinner("📡 Loading hierarchy data..."):
#                     hierarchy_success, hierarchy_data = get_user_hierarchy_info(bearer_token)
#                     # Cache the data
#                     st.session_state["hierarchy_data_cache"] = (hierarchy_success, hierarchy_data)
        
#         if hierarchy_success:
#             user_role = hierarchy_data.get("user_role", "Unknown")
#             user_email = hierarchy_data.get("user_email", "Unknown")
#             timestamp = hierarchy_data.get("timestamp", "Unknown")
            
#             st.success(f"**Role:** {user_role}")
#             st.info(f"**Email:** {user_email}")
#             st.caption(f"🕒 Last updated: {timestamp}")
            
#             # Show cache refresh status
#             if refresh_clicked and hierarchy_data.get("cache_refreshed"):
#                 st.info("🔄 Fresh data loaded from database")
            
#             has_hierarchy = hierarchy_data.get("has_hierarchy_access", False)
#             if has_hierarchy:
#                 hierarchy_info = hierarchy_data.get("hierarchy_access", {})
#                 managed_projects = hierarchy_info.get("managed_projects", [])
#                 all_team_members = hierarchy_info.get("all_team_members", [])
                
#                 st.success("🏗️ **Enhanced Access**")
#                 st.write(f"**Projects:** {len(managed_projects)}")
#                 st.write(f"**Team Members:** {len(all_team_members)}")
                
#                 with st.expander("📋 Managed Projects"):
#                     if managed_projects:
#                         for i, project in enumerate(managed_projects, 1):
#                             st.write(f"**{i}.** {project}")
#                     else:
#                         st.write("No projects assigned")
                        
#                 with st.expander("👥 Team Members"):
#                     if all_team_members:
#                         # Create a DataFrame for better display
#                         team_data = []
#                         for member in all_team_members:
#                             team_data.append({
#                                 "Name": member.get("name", "N/A"),
#                                 "Email": member.get("email", "N/A"),
#                                 "Role": member.get("role", "N/A")
#                             })
                        
#                         df = pd.DataFrame(team_data)
                        
#                         # Display as a nice table
#                         st.dataframe(
#                             df,
#                             use_container_width=True,
#                             hide_index=True,
#                             column_config={
#                                 "Name": st.column_config.TextColumn("👤 Name", width="medium"),
#                                 "Email": st.column_config.TextColumn("📧 Email", width="medium"),
#                                 "Role": st.column_config.TextColumn("🎭 Role", width="small")
#                             }
#                         )
                        
#                         # Summary statistics
#                         role_counts = df['Role'].value_counts()
#                         st.write("**📊 Team Composition:**")
#                         for role, count in role_counts.items():
#                             st.write(f"• **{role}:** {count} member(s)")
#                     else:
#                         st.write("No team members found")
                
#                 with st.expander("📈 Access Summary"):
#                     col1, col2 = st.columns(2)
                    
#                     with col1:
#                         st.metric(
#                             label="🎯 Managed Projects", 
#                             value=len(managed_projects)
#                         )
#                         st.metric(
#                             label="👥 Team Members", 
#                             value=len(all_team_members)
#                         )
                    
#                     with col2:
#                         hierarchy_breakdown = hierarchy_info.get("hierarchy_breakdown", {})
#                         excluded_roles = hierarchy_breakdown.get("excluded_roles", {})
                        
#                         total_excluded = (
#                             excluded_roles.get("admins_owners_excluded", 0) +
#                             excluded_roles.get("other_managers_excluded", 0) +
#                             excluded_roles.get("other_team_leads_excluded", 0)
#                         )
                        
#                         st.metric(
#                             label="🚫 Excluded Members", 
#                             value=total_excluded,
#                             help="Members excluded due to hierarchical access control"
#                         )
                        
#                         st.metric(
#                             label="✅ Latest Role Logic", 
#                             value="Applied" if hierarchy_info.get("latest_role_logic_applied") else "Not Applied"
#                         )
                    
#                     # Description
#                     description = hierarchy_info.get("description", "")
#                     if description:
#                         st.info(f"**Access Description:** {description}")
                        
#                 with st.expander("🔧 Technical Details"):
#                     # Show hierarchy breakdown in a cleaner way
#                     hierarchy_breakdown = hierarchy_info.get("hierarchy_breakdown", {})
#                     accessible_by_role = hierarchy_breakdown.get("accessible_by_role", {})
#                     excluded_roles = hierarchy_breakdown.get("excluded_roles", {})
                    
#                     st.write("**🎯 Accessible Roles Breakdown:**")
                    
#                     # Self access
#                     self_members = accessible_by_role.get("self", [])
#                     st.write(f"• **Self Access:** {len(self_members)} member(s)")
                    
#                     # Team leads access
#                     team_leads = accessible_by_role.get("team_leads", [])
#                     st.write(f"• **Team Leads:** {len(team_leads)} member(s)")
                    
#                     # Employees access
#                     employees = accessible_by_role.get("employees", [])
#                     st.write(f"• **Employees:** {len(employees)} member(s)")
                    
#                     st.write("**🚫 Excluded Due to Hierarchy:**")
#                     st.write(f"• **Admins/Owners:** {excluded_roles.get('admins_owners_excluded', 0)} member(s)")
#                     st.write(f"• **Other Managers:** {excluded_roles.get('other_managers_excluded', 0)} member(s)")
#                     st.write(f"• **Other Team Leads:** {excluded_roles.get('other_team_leads_excluded', 0)} member(s)")
                    
#                     # Show cache management info
#                     st.write("**🔄 Cache Information:**")
#                     st.write(f"• **Last Updated:** {timestamp}")
#                     st.write(f"• **Latest Role Logic:** {'✅ Applied' if hierarchy_info.get('latest_role_logic_applied') else '❌ Not Applied'}")
#                     cache_refreshed = hierarchy_data.get("cache_refreshed", False)
#                     st.write(f"• **Cache Status:** {'🔄 Refreshed' if cache_refreshed else '📦 Cached'}")
                    
#                     # Advanced cache controls
#                     st.write("**🛠️ Advanced Controls:**")
#                     if st.button("🗑️ Force Clear Cache & Refresh", help="Clear cache and load fresh data"):
#                         with st.spinner("🔄 Clearing cache and refreshing..."):
#                             # Clear session cache
#                             if "hierarchy_data_cache" in st.session_state:
#                                 del st.session_state["hierarchy_data_cache"]
                            
#                             # Force API cache refresh
#                             success, fresh_data = get_user_hierarchy_info(bearer_token, refresh_cache=True)
#                             if success:
#                                 st.session_state["hierarchy_data_cache"] = (success, fresh_data)
#                                 st.success("✅ Cache cleared and fresh data loaded!")
#                                 st.rerun()
#                             else:
#                                 st.error("❌ Failed to refresh cache")
                    
#                     # Show raw data in a collapsible section for debugging
#                     with st.expander("🔍 Raw Hierarchy Data (Debug)"):
#                         st.json(hierarchy_info)
#             else:
#                 st.info("📝 Standard Access")
#                 st.write(hierarchy_data.get("message", "Using standard access logic"))
                
#                 # Show refresh timestamp even for standard access
#                 timestamp = hierarchy_data.get("timestamp", "Unknown")
#                 st.caption(f"🕒 Checked: {timestamp}")
#         else:
#             st.error("❌ Could not retrieve user access info")
#             st.error(hierarchy_data)
    
#     # Initialize chat history
#     if "messages" not in st.session_state:
#         st.session_state.messages = []
    
#     # Main chat interface
#     st.subheader("💬 Chat Interface")
    
#     # Display chat history
#     chat_container = st.container()
#     with chat_container:
#         for message in st.session_state.messages:
#             if message["role"] == "user":
#                 with st.chat_message("user"):
#                     st.markdown(message["content"])
#             else:
#                 with st.chat_message("assistant"):
#                     st.markdown(message["content"])
                    
#                     # Show additional info if available
#                     if "timestamp" in message:
#                         st.caption(f"🕒 {message['timestamp']}")
#                     if "access_verification" in message:
#                         with st.expander("🔒 Access Verification"):
#                             st.text(message["access_verification"])
    
#     # Chat input
#     prompt = st.chat_input("Ask about worklog data, team performance, or project insights...")
    
#     if prompt:
#         # Add user message to chat history
#         st.session_state.messages.append({"role": "user", "content": prompt})
        
#         # Display user message
#         with st.chat_message("user"):
#             st.markdown(prompt)
        
#         # Send to API and display response
#         with st.chat_message("assistant"):
#             with st.spinner("Processing your request..."):
#                 success, response_data = send_chat_message(
#                     prompt, 
#                     bearer_token, 
#                     st.session_state.session_id
#                 )
                
#                 if success:
#                     response_text = response_data.get("response", "No response received")
#                     access_verification = response_data.get("access_verification", "")
#                     user_details = response_data.get("user_details", {})
                    
#                     st.markdown(response_text)
                    
#                     # Store assistant response
#                     assistant_message = {
#                         "role": "assistant",
#                         "content": response_text,
#                         "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#                         "access_verification": access_verification
#                     }
#                     st.session_state.messages.append(assistant_message)
                    
#                     # Show additional details in expander
#                     with st.expander("📊 Response Details"):
#                         col1, col2 = st.columns(2)
                        
#                         with col1:
#                             st.subheader("🔒 Access Verification")
#                             st.text(access_verification)
                            
#                         with col2:
#                             st.subheader("👤 User Details")
#                             st.json(user_details)
                            
#                         st.subheader("📋 Full Response Data")
#                         st.json(response_data)
                
#                 else:
#                     error_message = f"❌ **Error:** {response_data}"
#                     st.error(error_message)
                    
#                     # Store error message
#                     st.session_state.messages.append({
#                         "role": "assistant",
#                         "content": error_message,
#                         "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#                     })
    
#     # Sample queries section
#     with st.expander("💡 Sample Queries"):
#         st.markdown("**For Employees:**")
#         st.code("My worklog for last week")
#         st.code("My project activities this month")
#         st.code("My performance summary for July")
        
#         st.markdown("**For Team Leads/Managers:**")
#         st.code("Team performance this month")
#         st.code("Show my team's worklog summary")
#         st.code("Project Alpha performance analysis")
#         st.code("What is Manish working on currently?")
        
#         st.markdown("**For Owners:**")
#         st.code("Company-wide July analysis")
#         st.code("All projects performance summary")
#         st.code("Organization worklog insights")
        
#         st.markdown("**Time-based Queries:**")
#         st.code("June 2025 team report")
#         st.code("This month's summary")
#         st.code("Last month's analysis")
#         st.code("From June 15 to July 12")
        
#         st.markdown("**💡 Pro Tips:**")
#         st.info("🔄 Use the 'Refresh' button if you've been added to new projects or teams")
#         st.info("📅 Single month queries are always allowed (e.g., 'July 2025')")
#         st.info("🚫 Multi-month queries are blocked for cost control (e.g., 'last 6 months')")
    
#     # Footer
#     st.markdown("---")
#     col1, col2, col3 = st.columns(3)
    
#     with col1:
#         st.markdown("**Summary Agent v4.2.0**")
#         st.caption("Enhanced with Hierarchical Access Control")
    
#     with col2:
#         st.markdown(f"**Session:** `{st.session_state.session_id[:8]}...`")
#         st.caption(f"API: {API_BASE_URL}")
    
#     with col3:
#         if "hierarchy_data_cache" in st.session_state:
#             cache_status = "📦 Cached"
#         else:
#             cache_status = "🔄 Fresh"
#         st.markdown(f"**Hierarchy:** {cache_status}")
#         st.caption("Click refresh to update team data")

# if __name__ == "__main__":
#     main()

import streamlit as st
import requests
import json
import uuid
import pandas as pd
from datetime import datetime
import time

# Configure Streamlit page
st.set_page_config(
    page_title="Summary Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better typography and formatting with dark mode support
st.markdown("""
<style>
    /* Main content area improvements */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Light mode styles */
    [data-theme="light"] .chat-response {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        color: #374151;
    }
    
    [data-theme="light"] .formatted-content {
        color: #374151;
    }
    
    [data-theme="light"] .formatted-content h2 {
        color: #1f2937;
        border-bottom: 2px solid #3b82f6;
    }
    
    [data-theme="light"] .formatted-content h3,
    [data-theme="light"] .formatted-content h4 {
        color: #374151;
    }
    
    [data-theme="light"] .formatted-content strong {
        color: #1f2937;
    }
    
    /* Dark mode styles */
    [data-theme="dark"] .chat-response,
    .stApp[data-theme="dark"] .chat-response,
    html[data-theme="dark"] .chat-response {
        background-color: #1f2937 !important;
        border: 1px solid #374151 !important;
        color: #f3f4f6 !important;
    }
    
    [data-theme="dark"] .formatted-content,
    .stApp[data-theme="dark"] .formatted-content,
    html[data-theme="dark"] .formatted-content {
        color: #f3f4f6 !important;
    }
    
    [data-theme="dark"] .formatted-content h2,
    .stApp[data-theme="dark"] .formatted-content h2,
    html[data-theme="dark"] .formatted-content h2 {
        color: #ffffff !important;
        border-bottom: 2px solid #60a5fa !important;
    }
    
    [data-theme="dark"] .formatted-content h3,
    [data-theme="dark"] .formatted-content h4,
    .stApp[data-theme="dark"] .formatted-content h3,
    .stApp[data-theme="dark"] .formatted-content h4,
    html[data-theme="dark"] .formatted-content h3,
    html[data-theme="dark"] .formatted-content h4 {
        color: #e5e7eb !important;
    }
    
    [data-theme="dark"] .formatted-content strong,
    .stApp[data-theme="dark"] .formatted-content strong,
    html[data-theme="dark"] .formatted-content strong {
        color: #ffffff !important;
    }
    
    [data-theme="dark"] .formatted-content code,
    .stApp[data-theme="dark"] .formatted-content code,
    html[data-theme="dark"] .formatted-content code {
        background-color: #374151 !important;
        color: #f3f4f6 !important;
    }
    
    /* Fallback for when theme detection doesn't work - detect based on background */
    @media (prefers-color-scheme: dark) {
        .chat-response {
            background-color: #1f2937 !important;
            border: 1px solid #374151 !important;
            color: #f3f4f6 !important;
        }
        
        .formatted-content {
            color: #f3f4f6 !important;
        }
        
        .formatted-content h2 {
            color: #ffffff !important;
            border-bottom: 2px solid #60a5fa !important;
        }
        
        .formatted-content h3,
        .formatted-content h4 {
            color: #e5e7eb !important;
        }
        
        .formatted-content strong {
            color: #ffffff !important;
        }
        
        .formatted-content code {
            background-color: #374151 !important;
            color: #f3f4f6 !important;
        }
    }
    
    /* Universal styles that work in both modes */
    .chat-response {
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.2s ease;
    }
    
    .formatted-content {
        line-height: 1.7;
    }
    
    .formatted-content h2 {
    font-size: 1.25rem;
    font-weight: 700 !important;
    margin: 0.5rem 0 0.3rem 0;  /* Reduced from 1.5rem to 1rem */
    padding-bottom: 0.2rem;   /* Reduced from 0.5rem to 0.3rem */
    display: block !important;
    clear: both !important;
    }
    
    .formatted-content h3 {
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0.5rem 0 0.3rem 0;
    }
    
    .formatted-content h4 {
        font-size: 1rem;
        font-weight: 600;
        margin: 1rem 0 0.5rem 0;
    }
            
    .formatted-content p {
    margin: 0.2rem 0;  /* Reduced from 0.5rem to 0.2rem */
    line-height: 1.5;  /* Reduced from 1.7 to 1.5 */
    }
    
    .formatted-content ul {
        margin: 0.3rem 0 0.5rem 0;
        padding-left: 1.5rem;
    }
    
    .formatted-content li {
        margin-bottom: 0.2rem;
        line-height: 1.4;
    }
    
    .formatted-content strong {
        font-weight: 600;
    }
    
    .formatted-content code {
        padding: 0.2rem 0.4rem;
        border-radius: 3px;
        font-family: monospace;
        font-size: 0.9em;
    }
    
    /* Nested list improvements */
    .formatted-content ul ul {
        margin: 0.2rem 0;
        padding-left: 1.2rem;
    }
    
    .formatted-content ul ul li {
        margin-bottom: 0.2rem;
        list-style-type: circle;
    }
    
    /* Chat message improvements */
    .stChatMessage {
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* Button improvements */
    .stButton button {
        border-radius: 6px;
        transition: all 0.2s;
    }
    
    .stButton button:hover {
        transform: translateY(-1px);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Success/error message improvements */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 6px;
        border-left: 4px solid;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
    }
    
    /* Table improvements */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "https://mcp-summarization.minervaiotstaging.com"
CHAT_ENDPOINT = f"{API_BASE_URL}/chat"
HEALTH_ENDPOINT = f"{API_BASE_URL}/health"
HIERARCHY_ENDPOINT = f"{API_BASE_URL}/hierarchy/access"

def format_response_content(content):
    """
    Format the response content with better structure and bullet points
    Convert markdown to HTML for proper rendering with dark mode support
    """
    import re
    
    # Split content into lines
    lines = content.split('\n')
    formatted_lines = []
    in_list = False
    
    for line in lines:
        stripped_line = line.strip()
        
        # Skip empty lines but preserve them for spacing
        # Skip empty lines but preserve them for spacing
        if not stripped_line:
            if in_list:
                in_list = False
                formatted_lines.append('</ul>')
            # Only add line break if previous line wasn't a header
            # if formatted_lines and not formatted_lines[-1].startswith('<h'):
            #     formatted_lines.append('<br>')
            continue
        
        # Handle headers (##, ###, ####) - removed inline styles, using CSS classes
        if stripped_line.startswith('####'):
            if in_list:
                in_list = False
                formatted_lines.append('</ul>')
            header_text = stripped_line[4:].strip()
            formatted_lines.append(f'<h4>{header_text}</h4>')
            continue
        elif stripped_line.startswith('###'):
            if in_list:
                in_list = False
                formatted_lines.append('</ul>')
            header_text = stripped_line[3:].strip()
            formatted_lines.append(f'<h3>{header_text}</h3>')
            continue
        elif stripped_line.startswith('##') or '## ' in stripped_line:
            if in_list:
                in_list = False
                formatted_lines.append('</ul>')
            
            # Extract header text after ##
            if stripped_line.startswith('##'):
                header_text = stripped_line[2:].strip()
            else:
                header_text = stripped_line.split('## ', 1)[1].strip()
            
            formatted_lines.append(f'<h2><strong>{header_text}</strong></h2>')
            continue
        
        # Handle bullet points that start with •
        if stripped_line.startswith('•'):
            if not in_list:
                in_list = True
                formatted_lines.append('<ul>')
            # Process the bullet content for bold formatting
            bullet_content = stripped_line[1:].strip()
            bullet_content = process_text_formatting(bullet_content)
            formatted_lines.append(f'<li>{bullet_content}</li>')
            continue
        
        # Handle bullet points that start with *
        if stripped_line.startswith('*') and not stripped_line.startswith('**'):
            if not in_list:
                in_list = True
                formatted_lines.append('<ul>')
            # Convert * to • for consistency
            bullet_content = stripped_line[1:].strip()
            bullet_content = process_text_formatting(bullet_content)
            formatted_lines.append(f'<li>{bullet_content}</li>')
            continue
        
        # Handle sub-bullet points that start with - or are indented
        if stripped_line.startswith('-') or line.startswith('  ') or line.startswith('\t'):
            # This is likely a sub-bullet point
            bullet_content = stripped_line.lstrip('- \t')
            bullet_content = process_text_formatting(bullet_content)
            if not in_list:
                in_list = True
                formatted_lines.append('<ul>')
            formatted_lines.append(f'<li style="margin-left: 1rem; list-style-type: circle;">{bullet_content}</li>')
            continue
        
        # Regular text line
        if in_list and not stripped_line.startswith(('•', '*', '-', '#')):
            # This might be a continuation of a bullet point that got split
            # Check if previous line was a bullet point
            if formatted_lines and '<li' in formatted_lines[-1]:
                # Append to previous line (remove closing </li> and add content)
                formatted_lines[-1] = formatted_lines[-1].replace('</li>', f' {process_text_formatting(stripped_line)}</li>')
            else:
                in_list = False
                formatted_lines.append('</ul>')
                processed_text = process_text_formatting(stripped_line)
                formatted_lines.append(f'<p>{processed_text}</p>')
        else:
            if in_list:
                in_list = False
                formatted_lines.append('</ul>')
            processed_text = process_text_formatting(stripped_line)
            formatted_lines.append(f'<p>{processed_text}</p>')
    
    # Close any open lists
    if in_list:
        formatted_lines.append('</ul>')
    
    return '\n'.join(formatted_lines)

def process_text_formatting(text):
    """
    Convert markdown-style formatting to HTML with dark mode support
    """
    import re
    
    # Handle bold text (**text** or __text__)
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'__(.*?)__', r'<strong>\1</strong>', text)
    
    # Handle italic text (*text* or _text_)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    text = re.sub(r'_(.*?)_', r'<em>\1</em>', text)
    
    # Handle code snippets (`code`) - styling handled by CSS
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
    
    return text

def check_api_health():
    """Check if the API is running and healthy"""
    try:
        response = requests.get(HEALTH_ENDPOINT, timeout=5)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"API returned status code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return False, f"Connection error: {str(e)}"

def get_user_hierarchy_info(bearer_token, refresh_cache=False):
    """Get user hierarchy information from the API"""
    try:
        headers = {"Authorization": f"Bearer {bearer_token}"}
        params = {"refresh_cache": refresh_cache} if refresh_cache else {}
        
        response = requests.get(
            HIERARCHY_ENDPOINT, 
            headers=headers, 
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"Error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return False, f"Connection error: {str(e)}"

def send_chat_message(message, bearer_token, session_id):
    """Send a chat message to the API"""
    try:
        headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "message": message,
            "session_id": session_id
        }
        
        response = requests.post(
            CHAT_ENDPOINT, 
            headers=headers, 
            json=payload, 
            timeout=120  # Increased timeout for complex queries
        )
        
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"Error {response.status_code}: {response.text}"
            
    except requests.exceptions.RequestException as e:
        return False, f"Connection error: {str(e)}"

def display_formatted_response(content):
    """Display response with improved formatting using proper HTML conversion"""
    formatted_content = format_response_content(content)
    
    # Use custom CSS class for better formatting with proper HTML rendering
    st.markdown(f"""
    <div class="chat-response">
        <div class="formatted-content">
            {formatted_content}
        </div>
    </div>
    """, unsafe_allow_html=True)

def main():
    # Header with better styling
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0; margin-bottom: 2rem;">
        <h1 style="color: #f3f6f4; margin-bottom: 0.5rem;">🤖 Summary Agent</h1>
        <p style="color: #f3f6f4; font-size: 1.1rem; margin: 0;">Enhanced AI Assistant with Hierarchical Access Control</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # API Health Check
        st.subheader("🏥 API Status")
        health_status, health_data = check_api_health()
        
        if health_status:
            if isinstance(health_data, dict):
                api_status = health_data.get("status", "unknown")
                tunnel_active = health_data.get("tunnel_active", False)
                
                # Show status with appropriate color
                if api_status == "healthy":
                    st.success("✅ API is healthy")
                elif api_status == "degraded":
                    if not tunnel_active:
                        st.warning("⚠️ API running (SSH tunnel inactive)")
                        st.info("💡 SSH tunnel may connect automatically when needed")
                    else:
                        st.warning("⚠️ API status degraded")
                else:
                    st.info(f"ℹ️ API status: {api_status}")
                
                # Show key components status
                components = health_data.get("components", {})
                col1, col2 = st.columns(2)
                
                with col1:
                    fastapi_status = components.get("fastapi", "unknown")
                    if fastapi_status == "running":
                        st.success("🚀 FastAPI: Running")
                    else:
                        st.error(f"❌ FastAPI: {fastapi_status}")
                
                with col2:
                    tunnel_status = "Active" if tunnel_active else "Inactive"
                    tunnel_color = st.success if tunnel_active else st.info
                    tunnel_color(f"🔗 SSH: {tunnel_status}")
                
                # Production Safety Status
                production_safety = health_data.get("production_safety", {})
                with st.expander("🛡️ Production Safety"):
                    st.write("**Smart Limit System:**", production_safety.get("smart_limit_system", "unknown"))
                    st.write("**Hierarchy Control:**", production_safety.get("team_lead_manager_hierarchy", "unknown"))
                    st.write("**Date Range Limit:**", production_safety.get("date_range_limit", "unknown"))
                    st.write("**Cost Control:**", production_safety.get("cost_control", "unknown"))
                
                # Pipeline Status
                pipeline_status = health_data.get("pipeline_status", {})
                with st.expander("⚙️ Pipeline Status"):
                    for phase, status in pipeline_status.items():
                        phase_name = phase.replace("_", " ").title()
                        st.write(f"**{phase_name}:** {status}")
                
                # Agent Statistics
                agents = components.get("agents", {})
                if any(agents.values()):
                    with st.expander("🤖 Active Agents"):
                        st.write(f"**Verification Agents:** {agents.get('verification_agents', 0)}")
                        st.write(f"**Data Agents:** {agents.get('data_agents', 0)}")
                        st.write(f"**MCP Tools:** {agents.get('mcp_tools_instances', 0)}")
                else:
                    st.info("🤖 No active agent sessions")
                
                # Raw data for debugging (collapsed by default)
                with st.expander("🔧 Raw API Response (Debug)"):
                    st.json(health_data)
            else:
                st.success("✅ API is accessible")
        else:
            st.error(f"❌ API is not accessible")
            st.error(health_data)
            st.stop()
        
        # Authentication
        st.subheader("🔐 Authentication")
        bearer_token = st.text_input(
            "Bearer Token",
            type="password",
            help="Enter your JWT bearer token for API access"
        )
        
        if not bearer_token:
            st.warning("⚠️ Please enter your bearer token to continue")
            st.stop()
        
        # Session Management
        st.subheader("📝 Session")
        if "session_id" not in st.session_state:
            st.session_state.session_id = str(uuid.uuid4())
        
        st.text(f"Session ID: {st.session_state.session_id[:8]}...")
        
        if st.button("🔄 New Session"):
            st.session_state.session_id = str(uuid.uuid4())
            st.session_state.messages = []
            # Clear hierarchy cache when starting new session
            if "hierarchy_data_cache" in st.session_state:
                del st.session_state["hierarchy_data_cache"]
            st.rerun()
        
        # User Hierarchy Information
        st.subheader("👤 User Access")
        
        # Add refresh button
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write("**Hierarchy Information**")
        with col2:
            refresh_clicked = st.button("🔄 Refresh", help="Refresh hierarchy data from database")
        
        # Get hierarchy info (with refresh if button was clicked)
        if refresh_clicked:
            with st.spinner("🔄 Refreshing hierarchy data..."):
                hierarchy_success, hierarchy_data = get_user_hierarchy_info(bearer_token, refresh_cache=True)
                # Clear any cached data
                if "hierarchy_data_cache" in st.session_state:
                    del st.session_state["hierarchy_data_cache"]
                # Cache the fresh data
                st.session_state["hierarchy_data_cache"] = (hierarchy_success, hierarchy_data)
                
                if hierarchy_success:
                    st.success("✅ Hierarchy data refreshed successfully!")
                else:
                    st.error("❌ Failed to refresh hierarchy data")
        else:
            # Use cached data if available, otherwise fetch fresh
            if "hierarchy_data_cache" in st.session_state:
                hierarchy_success, hierarchy_data = st.session_state["hierarchy_data_cache"]
                st.info("📦 Using cached hierarchy data")
            else:
                with st.spinner("📡 Loading hierarchy data..."):
                    hierarchy_success, hierarchy_data = get_user_hierarchy_info(bearer_token)
                    # Cache the data
                    st.session_state["hierarchy_data_cache"] = (hierarchy_success, hierarchy_data)
        
        if hierarchy_success:
            user_role = hierarchy_data.get("user_role", "Unknown")
            user_email = hierarchy_data.get("user_email", "Unknown")
            timestamp = hierarchy_data.get("timestamp", "Unknown")
            
            st.success(f"**Role:** {user_role}")
            st.info(f"**Email:** {user_email}")
            st.caption(f"🕒 Last updated: {timestamp}")
            
            # Show cache refresh status
            if refresh_clicked and hierarchy_data.get("cache_refreshed"):
                st.info("🔄 Fresh data loaded from database")
            
            has_hierarchy = hierarchy_data.get("has_hierarchy_access", False)
            if has_hierarchy:
                hierarchy_info = hierarchy_data.get("hierarchy_access", {})
                managed_projects = hierarchy_info.get("managed_projects", [])
                all_team_members = hierarchy_info.get("all_team_members", [])
                
                st.success("🏗️ **Enhanced Access**")
                st.write(f"**Projects:** {len(managed_projects)}")
                st.write(f"**Team Members:** {len(all_team_members)}")
                
                with st.expander("📋 Managed Projects"):
                    if managed_projects:
                        for i, project in enumerate(managed_projects, 1):
                            st.write(f"**{i}.** {project}")
                    else:
                        st.write("No projects assigned")
                        
                with st.expander("👥 Team Members"):
                    if all_team_members:
                        # Create a DataFrame for better display
                        team_data = []
                        for member in all_team_members:
                            team_data.append({
                                "Name": member.get("name", "N/A"),
                                "Email": member.get("email", "N/A"),
                                "Role": member.get("role", "N/A")
                            })
                        
                        df = pd.DataFrame(team_data)
                        
                        # Display as a nice table
                        st.dataframe(
                            df,
                            use_container_width=True,
                            hide_index=True,
                            column_config={
                                "Name": st.column_config.TextColumn("👤 Name", width="medium"),
                                "Email": st.column_config.TextColumn("📧 Email", width="medium"),
                                "Role": st.column_config.TextColumn("🎭 Role", width="small")
                            }
                        )
                        
                        # Summary statistics
                        role_counts = df['Role'].value_counts()
                        st.write("**📊 Team Composition:**")
                        for role, count in role_counts.items():
                            st.write(f"• **{role}:** {count} member(s)")
                    else:
                        st.write("No team members found")
                
                with st.expander("📈 Access Summary"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric(
                            label="🎯 Managed Projects", 
                            value=len(managed_projects)
                        )
                        st.metric(
                            label="👥 Team Members", 
                            value=len(all_team_members)
                        )
                    
                    with col2:
                        hierarchy_breakdown = hierarchy_info.get("hierarchy_breakdown", {})
                        excluded_roles = hierarchy_breakdown.get("excluded_roles", {})
                        
                        total_excluded = (
                            excluded_roles.get("admins_owners_excluded", 0) +
                            excluded_roles.get("other_managers_excluded", 0) +
                            excluded_roles.get("other_team_leads_excluded", 0)
                        )
                        
                        st.metric(
                            label="🚫 Excluded Members", 
                            value=total_excluded,
                            help="Members excluded due to hierarchical access control"
                        )
                        
                        st.metric(
                            label="✅ Latest Role Logic", 
                            value="Applied" if hierarchy_info.get("latest_role_logic_applied") else "Not Applied"
                        )
                    
                    # Description
                    description = hierarchy_info.get("description", "")
                    if description:
                        st.info(f"**Access Description:** {description}")
                        
                with st.expander("🔧 Technical Details"):
                    # Show hierarchy breakdown in a cleaner way
                    hierarchy_breakdown = hierarchy_info.get("hierarchy_breakdown", {})
                    accessible_by_role = hierarchy_breakdown.get("accessible_by_role", {})
                    excluded_roles = hierarchy_breakdown.get("excluded_roles", {})
                    
                    st.write("**🎯 Accessible Roles Breakdown:**")
                    
                    # Self access
                    self_members = accessible_by_role.get("self", [])
                    st.write(f"• **Self Access:** {len(self_members)} member(s)")
                    
                    # Team leads access
                    team_leads = accessible_by_role.get("team_leads", [])
                    st.write(f"• **Team Leads:** {len(team_leads)} member(s)")
                    
                    # Employees access
                    employees = accessible_by_role.get("employees", [])
                    st.write(f"• **Employees:** {len(employees)} member(s)")
                    
                    st.write("**🚫 Excluded Due to Hierarchy:**")
                    st.write(f"• **Admins/Owners:** {excluded_roles.get('admins_owners_excluded', 0)} member(s)")
                    st.write(f"• **Other Managers:** {excluded_roles.get('other_managers_excluded', 0)} member(s)")
                    st.write(f"• **Other Team Leads:** {excluded_roles.get('other_team_leads_excluded', 0)} member(s)")
                    
                    # Show cache management info
                    st.write("**🔄 Cache Information:**")
                    st.write(f"• **Last Updated:** {timestamp}")
                    st.write(f"• **Latest Role Logic:** {'✅ Applied' if hierarchy_info.get('latest_role_logic_applied') else '❌ Not Applied'}")
                    cache_refreshed = hierarchy_data.get("cache_refreshed", False)
                    st.write(f"• **Cache Status:** {'🔄 Refreshed' if cache_refreshed else '📦 Cached'}")
                    
                    # Advanced cache controls
                    st.write("**🛠️ Advanced Controls:**")
                    if st.button("🗑️ Force Clear Cache & Refresh", help="Clear cache and load fresh data"):
                        with st.spinner("🔄 Clearing cache and refreshing..."):
                            # Clear session cache
                            if "hierarchy_data_cache" in st.session_state:
                                del st.session_state["hierarchy_data_cache"]
                            
                            # Force API cache refresh
                            success, fresh_data = get_user_hierarchy_info(bearer_token, refresh_cache=True)
                            if success:
                                st.session_state["hierarchy_data_cache"] = (success, fresh_data)
                                st.success("✅ Cache cleared and fresh data loaded!")
                                st.rerun()
                            else:
                                st.error("❌ Failed to refresh cache")
                    
                    # Show raw data in a collapsible section for debugging
                    with st.expander("🔍 Raw Hierarchy Data (Debug)"):
                        st.json(hierarchy_info)
            else:
                st.info("📝 Standard Access")
                st.write(hierarchy_data.get("message", "Using standard access logic"))
                
                # Show refresh timestamp even for standard access
                timestamp = hierarchy_data.get("timestamp", "Unknown")
                st.caption(f"🕒 Checked: {timestamp}")
        else:
            st.error("❌ Could not retrieve user access info")
            st.error(hierarchy_data)
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Main chat interface
    st.subheader("💬 Chat Interface")
    
    # Display chat history with improved formatting
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.markdown(message["content"])
            else:
                with st.chat_message("assistant"):
                    # Use the improved formatting function
                    display_formatted_response(message["content"])
                    
                    # Show additional info if available
                    if "timestamp" in message:
                        st.caption(f"🕒 {message['timestamp']}")
                    if "access_verification" in message:
                        with st.expander("🔒 Access Verification"):
                            st.text(message["access_verification"])
    
    # Chat input
    prompt = st.chat_input("Ask about worklog data, team performance, or project insights...")
    
    if prompt:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Send to API and display response
        with st.chat_message("assistant"):
            with st.spinner("Processing your request..."):
                success, response_data = send_chat_message(
                    prompt, 
                    bearer_token, 
                    st.session_state.session_id
                )
                
                if success:
                    response_text = response_data.get("response", "No response received")
                    access_verification = response_data.get("access_verification", "")
                    user_details = response_data.get("user_details", {})
                    
                    # Use the improved formatting function
                    display_formatted_response(response_text)
                    
                    # Store assistant response
                    assistant_message = {
                        "role": "assistant",
                        "content": response_text,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "access_verification": access_verification
                    }
                    st.session_state.messages.append(assistant_message)
                    
                    # Show additional details in expander
                    with st.expander("📊 Response Details"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("🔒 Access Verification")
                            st.text(access_verification)
                            
                        with col2:
                            st.subheader("👤 User Details")
                            st.json(user_details)
                            
                        st.subheader("📋 Full Response Data")
                        st.json(response_data)
                
                else:
                    error_message = f"❌ **Error:** {response_data}"
                    st.error(error_message)
                    
                    # Store error message
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_message,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
    
    # Sample queries section with better styling
    with st.expander("💡 Sample Queries", expanded=False):
        st.markdown("### 👤 For Employees:")
        sample_queries_employee = [
            "My worklog for last week",
            "My project activities this month", 
            "My performance summary for July"
        ]
        for query in sample_queries_employee:
            if st.button(f"📋 {query}", key=f"emp_{query}"):
                st.session_state.temp_query = query
                st.rerun()
        
        st.markdown("### 🏢 For Team Leads/Managers:")
        sample_queries_manager = [
            "Team performance this month",
            "Show my team's worklog summary",
            "Project Alpha performance analysis",
            "What is Manish working on currently?"
        ]
        for query in sample_queries_manager:
            if st.button(f"📋 {query}", key=f"mgr_{query}"):
                st.session_state.temp_query = query
                st.rerun()
        
        st.markdown("### 🏛️ For Owners:")
        sample_queries_owner = [
            "Company-wide July analysis",
            "All projects performance summary",
            "Organization worklog insights"
        ]
        for query in sample_queries_owner:
            if st.button(f"📋 {query}", key=f"own_{query}"):
                st.session_state.temp_query = query
                st.rerun()
        
        st.markdown("### 📅 Time-based Queries:")
        sample_queries_time = [
            "June 2025 team report",
            "This month's summary",
            "Last month's analysis",
            "From June 15 to July 12"
        ]
        for query in sample_queries_time:
            if st.button(f"📋 {query}", key=f"time_{query}"):
                st.session_state.temp_query = query
                st.rerun()
        
        # Handle clicked sample query
        if hasattr(st.session_state, 'temp_query'):
            query = st.session_state.temp_query
            del st.session_state.temp_query
            
            # Add to chat and process
            st.session_state.messages.append({"role": "user", "content": query})
            
            # Process the query automatically
            with st.spinner("Processing your request..."):
                success, response_data = send_chat_message(
                    query, 
                    bearer_token, 
                    st.session_state.session_id
                )
                
                if success:
                    response_text = response_data.get("response", "No response received")
                    access_verification = response_data.get("access_verification", "")
                    
                    # Store assistant response
                    assistant_message = {
                        "role": "assistant",
                        "content": response_text,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "access_verification": access_verification
                    }
                    st.session_state.messages.append(assistant_message)
                    st.rerun()
        
        st.markdown("---")
        st.markdown("### 💡 Pro Tips:")
        tips = [
            "🔄 Use the 'Refresh' button if you've been added to new projects or teams",
            "📅 Single month queries are always allowed (e.g., 'July 2025')",
            "🚫 Multi-month queries are blocked for cost control (e.g., 'last 6 months')",
            "🎯 Be specific with names and projects for better results",
            "⏰ Include time periods to focus your queries"
        ]
        
        for tip in tips:
            st.info(tip)
    
    # Footer with better styling
    st.markdown("---")
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 1rem 0; color: #6b7280;">
        <div>
            <strong>Summary Agent v4.2.0</strong><br>
            <small>Enhanced with Hierarchical Access Control</small>
        </div>
        <div style="text-align: center;">
            <strong>Session:</strong> <code>{}</code><br>
            <small>API: {}</small>
        </div>
        <div style="text-align: right;">
            <strong>Hierarchy:</strong> {}<br>
            <small>Click refresh to update team data</small>
        </div>
    </div>
    """.format(
        st.session_state.session_id[:8] + "...",
        API_BASE_URL,
        "📦 Cached" if "hierarchy_data_cache" in st.session_state else "🔄 Fresh"
    ), unsafe_allow_html=True)

if __name__ == "__main__":
    main()

















