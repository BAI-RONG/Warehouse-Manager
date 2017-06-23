<%@ page language="java" contentType="text/html; charset=utf-8"
    pageEncoding="utf-8"%>

<body>
	
    	<div data-options="region:'center',title:''" id="center" class="easyui-layout" fit=true>
     		<div id="west"  data-options="region:'west',title:'导航栏',split:true"  style="width:180px;"  href="">
    			 <div id="menu" class="easyui-accordion"  style="margin-top: 0px;margin-left: 0px;" >
	    			  <div title="工具管理"  style="overflow:auto;padding:10px;">
    	  				<ul>
	         				<li id="tool_info" title="tool-search">查询及借用</li>
	         				<li id="tool_info" title="info-modify">借用情况</li>
	         				<li id="tool_info" title="info-modify">工具入库</li>
	        			</ul>
	        			</div>
	     
				</div>				    
    			    
    		</div>   
    		<div    region="center"  fit=true>  
					<div id="p" class="easyui-panel" title="" style="height:800;padding:10px;background:white;"  
			          closable=false   minimizable=false maximizable=false border=false>
			        	
					</div> 
	  		</div>
     			
    </div>
		
    
  <script type="text/javascript">
$('#tool_info').click(
		 function(){
			 
				 var src = $(this).attr('title');
				 
				 var title = $(this).html();
				 var panel=$("#p");
				 panel.panel({
						title:title,
						href:src
					})
					
				}
			
		);


</script>
  
</body>
