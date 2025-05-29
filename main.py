from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with API key from .env
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please check your .env file.")

client = OpenAI(api_key=api_key)

# Your MCP SSE endpoint from .env
MCP_ENDPOINT = os.getenv('MCP_ENDPOINT')
if not MCP_ENDPOINT:
    raise ValueError("MCP_ENDPOINT not found in environment variables. Please check your .env file.")

def query_with_mcp(question: str):
    """Query using OpenAI Responses API with MCP tools"""
    
    print(f"\nQuerying: {question}")
    print("-" * 40)
    
    try:
        resp = client.responses.create(
            model="gpt-4.1",  # or "gpt-4o"
            tools=[
                {
                    "type": "mcp",
                    "server_label": "customgpt_rag",
                    "server_url": MCP_ENDPOINT,
                    "require_approval": "never",  # Skip approvals for faster execution
                }
            ],
            input=question,
        )
        
        print("Response:")
        print(resp.output_text)
        
        # Comprehensive debugging of the response
        print("\n" + "="*60)
        print("🔍 DEBUG INFORMATION")
        print("="*60)
        
        print(f"📋 Response ID: {resp.id}")
        print(f"🤖 Model used: {resp.model}")
        print(f"💰 Token usage: {resp.usage.input_tokens} in, {resp.usage.output_tokens} out, {resp.usage.total_tokens} total")
        print(f"📊 Output items: {len(resp.output) if resp.output else 0}")
        
        # Analyze MCP tools discovered
        mcp_tools_items = [item for item in (resp.output or []) if hasattr(item, 'type') and item.type == 'mcp_list_tools']
        mcp_call_items = [item for item in (resp.output or []) if hasattr(item, 'type') and item.type == 'mcp_call']
        
        if mcp_tools_items:
            print(f"\n🔧 MCP TOOLS DISCOVERED: {len(mcp_tools_items)} server(s)")
            for i, tools_item in enumerate(mcp_tools_items):
                print(f"  Server {i+1}: '{tools_item.server_label}'")
                if hasattr(tools_item, 'tools') and tools_item.tools:
                    print(f"    Available tools: {len(tools_item.tools)}")
                    for j, tool in enumerate(tools_item.tools[:5]):  # Show first 5 tools
                        print(f"      {j+1}. {tool.name}")
                        if hasattr(tool, 'description') and tool.description:
                            # Show first line of description
                            desc_line = tool.description.split('\n')[0][:80]
                            print(f"         → {desc_line}{'...' if len(tool.description) > 80 else ''}")
                    if len(tools_item.tools) > 5:
                        print(f"      ... and {len(tools_item.tools) - 5} more tools")
                else:
                    print(f"    ❌ No tools found")
        else:
            print(f"\n❌ NO MCP TOOLS DISCOVERED")
            
        if mcp_call_items:
            print(f"\n🔄 MCP TOOLS CALLED: {len(mcp_call_items)}")
            for i, call_item in enumerate(mcp_call_items):
                print(f"\n  📞 Call {i+1}: '{call_item.name}'")
                print(f"     Server: {call_item.server_label if hasattr(call_item, 'server_label') else 'Unknown'}")
                
                # Show detailed input
                if hasattr(call_item, 'arguments') and call_item.arguments:
                    print(f"     📥 INPUT:")
                    try:
                        import json
                        args_dict = json.loads(call_item.arguments)
                        for key, value in args_dict.items():
                            if isinstance(value, str) and len(value) > 100:
                                print(f"       {key}: {value[:100]}...")
                            else:
                                print(f"       {key}: {value}")
                    except:
                        print(f"       Raw: {call_item.arguments}")
                else:
                    print(f"     📥 INPUT: None")
                
                # Show detailed output
                if hasattr(call_item, 'output') and call_item.output:
                    print(f"     📤 OUTPUT:")
                    output_str = str(call_item.output)
                    if len(output_str) > 500:
                        print(f"       {output_str[:500]}...")
                        print(f"       [Output truncated - full length: {len(output_str)} characters]")
                    else:
                        print(f"       {output_str}")
                else:
                    print(f"     📤 OUTPUT: None")
                
                # Show any errors
                if hasattr(call_item, 'error') and call_item.error:
                    print(f"     ❌ ERROR: {call_item.error}")
                else:
                    print(f"     ✅ Status: Success")
                
                print("     " + "-" * 50)
        else:
            print(f"\n⚠️  NO MCP TOOLS CALLED")
            if mcp_tools_items:
                print(f"    The model had access to MCP tools but chose not to use them for this query.")
                print(f"    This might be because the model felt it could answer from its general knowledge.")
                print(f"    Try asking more specific questions about your knowledge base or documents.")
        
        # Summary
        print(f"\n📊 SUMMARY:")
        print(f"  🔧 Tools available: {sum(len(item.tools) if hasattr(item, 'tools') and item.tools else 0 for item in mcp_tools_items)}")
        print(f"  🔄 Tools called: {len(mcp_call_items)}")
        print(f"  ✅ MCP integration: {'Working!' if mcp_tools_items else 'Failed - no tools discovered'}")
        
        # Optional: Show complete raw data for MCP calls (uncomment if needed for deep debugging)
        # if mcp_call_items:
        #     print(f"\n🔬 RAW MCP CALL DATA:")
        #     for i, call_item in enumerate(mcp_call_items):
        #         print(f"  Call {i+1} raw data:")
        #         for attr in dir(call_item):
        #             if not attr.startswith('_'):
        #                 try:
        #                     value = getattr(call_item, attr)
        #                     if not callable(value):
        #                         print(f"    {attr}: {value}")
        #                 except:
        #                     pass
        #         print("    " + "-" * 40)
        
        return resp
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        print(f"Full traceback:\n{traceback.format_exc()}")
        return None

def main():
    """Main function to run queries"""
    
    queries = [
        "market volatility",
        "What specific financial documents or data do you have access to in your knowledge base?",
        "Please query your knowledge base about recent market trends and provide a detailed analysis"
    ]
    
    for query in queries:
        response = query_with_mcp(query)
        print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    main()
