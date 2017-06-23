<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html PUBLIC >
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Tool Warehouse System</title>
<jsp:include page="/commons/common-js.jsp"></jsp:include>
<style type="text/css">
	.content {
		padding: 10px 10px 10px 10px;
	}
</style>
</head>
<body class="easyui-layout" id="body">
	
    <div data-options="region:'north',title:''" style="height:50px;" >    		
			<tr >
			<td><p style="float:right;padding-right:100px">欢迎${user.name} : ${user.id}登录       
			</p>
			<td><p style="float:right;padding-right:50px"><a href="/logout">退出</a></p></td>
			</td>
			</tr>
			<br/>
	    	<tr id="menu"  style="margin-top: 20px;margin-left: 50px;background-image: url('/images/head.PNG')">
    		<td> <a title="first" style="margin-center: 20px;margin-left: 20px;"> &nbsp 首页 &nbsp </a></td>
    		<td> <a title="base-info" style="margin-center: 20px;margin-left: 200px;"> &nbsp 个人信息 &nbsp </a></td>
    		<td> <a title="tool-info"  style="margin-center: 20px;margin-left: 50px;">  &nbsp 工具信息  </a>  </td>
    		</tr>
    </div>
    <div data-options="region:'center',title:''" id="center" class="easyui-layout">
    	<div id="main" class="easyui-panel" title="" style="height:800;padding:10px;background:white;"  
			          closable=false   minimizable=false maximizable=false border=false href="first">
     		<div id="west"  data-options="region:'west',title:'导航栏',split:true"  style="width:180px;"  href="">
    			    
		    </div>   
    		<div data-options="region:'center',title:''" id="center" class="easyui-layout">
  			
    		</div>
			</div>
     			
    </div>
   
<script type="text/javascript">

$(function(){
	
	$('a[title]').click(function(){
			var src = $(this).attr('title');
			var title = $(this).html();
			 var panel=$("#main");
			 panel.panel({
					href:src
				})
				
			

	});

	
})

</script>
</body>
</html>