<%@ page language="java" contentType="text/html; charset=utf-8"
    pageEncoding="utf-8"%>
<body>
<%@ page trimDirectiveWhitespaces="true" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>
<div  id="plist">
			
						
					
						<c:forEach items="${itemList}" var="item">
						
						
						<div style="border:2px solid,float:left,width:70,height:100">
							
								<div >
									<a href="/item/${item.id}.html">
										<img width="70" height="80" src="${item.image}" />
									</a>
								</div>
								<div style="width:10,height:20,overflow:hidden">
										${item.name}
									
								</div>
								
							</div>
							
								
							
					</c:forEach>
						</ul>
			</div>
		
</body>
</html>