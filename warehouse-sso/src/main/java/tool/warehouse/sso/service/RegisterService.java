package tool.warehouse.sso.service;

import tool.warehouse.common.pojo.WarehouseResult;
import tool.warehouse.pojo.User;

public interface RegisterService {
		public WarehouseResult checkData(String id);
		public WarehouseResult register(User user);
}
