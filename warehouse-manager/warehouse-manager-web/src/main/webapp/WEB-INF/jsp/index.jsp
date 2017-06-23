<%@ page language="java" contentType="text/html; charset=utf-8"
    pageEncoding="utf-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>后台管理系统</title>
<jsp:include page="/commons/common-js.jsp"></jsp:include>
<style type="text/css">
	.content {
		padding: 10px 10px 10px 10px;
	}
</style>
</head>
<body class="easyui-layout" id="body">

		<div id="north" data-options="region:'north',title:'',border:'true'" style="height:60px;" >
				
				<h2 align="center">后台管理系统</h2>
				
		</div>
		
		
		<div id="navigation" data-options="region:'west',title:'navigation',border:'true'" style="width:200px">
				
				<div id="menu" class="easyui-accordion" style="width:200px;height:160px;" animate=false selected=false>  
    				<div title="工具管理"  style="overflow:auto;padding:10px;">  
        			<ul>
	         		<li ><a value="item-add">新增工具</a></li>
	         		<li><br></li>
	         		<li><a value="item-list">查询工具</a></li>
	         		</ul>		  
    				</div>  
    				<div title="工具类管理"  style="padding:10px;">  
        			<ul>
	         		<li ><a value="/item-category">新增工具</a></li>
	         		<li><br></li>
	         		<li><a value="item-content">查询工具</a></li>
	         		</ul>
    				</div>    
				</div>     
		</div>
		<div id = "center" data-options="region:'center',border:false,title:''">
			<div id="p" class="easyui-panel" title="" style="height:800;padding:10px;background:white;"  
	          closable=false   minimizable=false maximizable=false border=false >
	        	
	            
			</div>  
		</div>

<script type="text/javascript">

$(function(){
	$('a').click(
			function(){
				var src=$(this).attr('value');
				var title=$(this).text();
				var panel = $("#p");
				panel.panel({
					title:title,
					href:src
				})
			}
			);
});

</script>
</body>

</html>