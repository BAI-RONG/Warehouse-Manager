<%@ page language="java" contentType="text/html; charset=utf-8"
    pageEncoding="utf-8"%>

<body >
	
	<div data-options="region:'center',title:''" id="center" class="easyui-layout" fit=true border=false>

     		<div id="west"  data-options="region:'west',title:'导航栏',split:true"  style="width:180px;"  href="">
    		<div id="menu" class="easyui-accordion"  style="margin-top: 0px;margin-left: 0px;" >
    	  <div title="用户管理"  style="overflow:auto;padding:10px;">
    	  <ul>
	         		<li> <a name="info" title="info-show">基本信息</a></li>
	         		<li > <a name="info" title="info-modify">信息修改</a></li>
	        </ul>
	        </div>
	     
	</div>				    
            </div>   

		

     			
    </div>
	
    
<script type="text/javascript">
$(function(){
	$("[name='info']").click(
			function(){
			var src = $(this).attr('title');
			$('#center').layout('remove','center');
			$('#center').layout('add',{   
			    href:'/info/src',   
			    split:true,
			    region:'center'
			})
			}); 
})
</script>
</body>
</html>
