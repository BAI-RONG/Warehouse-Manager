<%@ page language="java" contentType="text/html; charset=utf-8"
    pageEncoding="utf-8"%>
<body>

<div id="cc" class="easyui-layout" style="width:950px;height:430px;">  
    	<div region="north"  split="true" style="height:100px;line-height:100px;padding-left:100px" >
    	
    		<td >
    		<tr>工具查询: </tr>
    		<tr><input id="key" type="text" style="height:20,width:160" class="easyui-textbox" required="true"/></tr>
    		<tr><a href="javascript:void(0)" class="easyui-linkbutton" onclick="submitForm()">搜索</a></tr>
    		</td>
    	
    	</div>  
    
    <div id="center" region="center" title="查询结果" style="padding:5px;background:#eee;height:350px">
		    <div id="result" class="easyui-panel" title="" style="height:800;padding:10px;background:white;"  
			          closable=false   minimizable=false maximizable=false border=false >
			        	
					</div> 
    </div>
      
	</div>	  
<script type="text/javascript">


function submitForm(){
	var panel=$("#result")
	panel.panel({
		href:"search?q="+$("#key").val()
	}
	)
	
}


</script>

</body>
</html>
