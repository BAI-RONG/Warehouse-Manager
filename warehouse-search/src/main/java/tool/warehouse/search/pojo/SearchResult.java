package tool.warehouse.search.pojo;

import java.util.List;

public class SearchResult {
	private List<SearchItem> itemList;
	private Long resordCount;
	private int pageCount;
	private int curPage;
	public List<SearchItem> getItemList() {
		return itemList;
	}
	public void setItemList(List<SearchItem> itemList) {
		this.itemList = itemList;
	}
	public Long getResordCount() {
		return resordCount;
	}
	public void setResordCount(Long resordCount) {
		this.resordCount = resordCount;
	}
	public int getPageCount() {
		return pageCount;
	}
	public void setPageCount(int pageCount) {
		this.pageCount = pageCount;
	}
	public int getCurPage() {
		return curPage;
	}
	public void setCurPage(int curPage) {
		this.curPage = curPage;
	}
	
}
