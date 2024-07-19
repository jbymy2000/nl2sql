# <公司表>
```sql
CREATE TABLE companies (
    company_id INT AUTO_INCREMENT PRIMARY KEY,  -- 公司ID，自增主键
    company_name VARCHAR(255) NOT NULL,         -- 公司名称
    address VARCHAR(255),                       -- 地址
    city VARCHAR(100),                          -- 城市
    state VARCHAR(100),                         -- 州/省
    postal_code VARCHAR(20),                    -- 邮政编码
    country VARCHAR(100),                       -- 国家
    phone_number VARCHAR(20),                   -- 联系电话
    email VARCHAR(100),                         -- 电子邮件
    website VARCHAR(255),                       -- 公司网站
    founded_date DATE,                          -- 成立日期
    industry VARCHAR(100),                      -- 行业
    number_of_employees INT,                    -- 员工数量
    revenue DECIMAL(15, 2),                     -- 收入
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 创建时间，默认当前时间
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP -- 更新时间
);

```

# <用户表>
```sql
CREATE TABLE ride_sharing_users (
    id INT AUTO_INCREMENT PRIMARY KEY,      -- 用户ID，自增主键
    username VARCHAR(50) NOT NULL UNIQUE,   -- 用户名，唯一
    email VARCHAR(100) NOT NULL UNIQUE,     -- 邮箱，唯一
    password CHAR(60) NOT NULL,             -- 密码，使用更安全的哈希算法（例如 bcrypt）
    phone_number VARCHAR(15) NOT NULL UNIQUE, -- 手机号码，唯一
    first_name VARCHAR(50) NOT NULL,        -- 名
    last_name VARCHAR(50) NOT NULL,         -- 姓
    date_of_birth DATE,                     -- 出生日期
    gender ENUM('Male', 'Female', 'Other'), -- 性别
    profile_picture_url VARCHAR(255),       -- 头像URL
    home_address VARCHAR(255),              -- 家庭地址
    work_address VARCHAR(255),              -- 工作地址
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 创建时间，默认当前时间
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP -- 更新时间
);

```
# <订单表>
```sql
CREATE TABLE ride_orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,        -- 订单ID，自增主键
    user_id INT NOT NULL,                           -- 用户ID，外键
    driver_id INT NOT NULL,                         -- 司机ID，外键
    pickup_location VARCHAR(255) NOT NULL,          -- 起点位置
    dropoff_location VARCHAR(255) NOT NULL,         -- 终点位置
    distance DECIMAL(5, 2) NOT NULL,                -- 距离，单位：公里
    price DECIMAL(10, 2) NOT NULL,                  -- 价格
    status ENUM('requested', 'accepted', 'completed', 'cancelled') NOT NULL, -- 订单状态
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 创建时间，默认当前时间
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- 更新时间
    CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES ride_sharing_users(id), -- 用户表外键
    CONSTRAINT fk_driver_id FOREIGN KEY (driver_id) REFERENCES drivers(id) -- 司机表外键（假设有司机表）
);

```
# <司机表>
```sql
CREATE TABLE drivers (
    driver_id INT AUTO_INCREMENT PRIMARY KEY,     -- 司机ID，自增主键
    username VARCHAR(50) NOT NULL UNIQUE,         -- 用户名，唯一
    email VARCHAR(100) NOT NULL UNIQUE,           -- 邮箱，唯一
    password CHAR(60) NOT NULL,                   -- 密码，使用更安全的哈希算法（例如 bcrypt）
    phone_number VARCHAR(15) NOT NULL UNIQUE,     -- 手机号码，唯一
    first_name VARCHAR(50) NOT NULL,              -- 名
    last_name VARCHAR(50) NOT NULL,               -- 姓
    license_number VARCHAR(50) NOT NULL UNIQUE,   -- 驾照号码，唯一
    vehicle_plate VARCHAR(20) NOT NULL UNIQUE,    -- 车牌号，唯一
    vehicle_type VARCHAR(50) NOT NULL,            -- 车辆类型
    rating DECIMAL(3, 2) DEFAULT 5.00,            -- 评分，默认值为5.00
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 创建时间，默认当前时间
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP -- 更新时间
);
```