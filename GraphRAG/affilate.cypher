CREATE (v1:Vendor {id: 'v_001', name: 'Apple Vietnam'})
CREATE (v2:Vendor {id: 'v_002', name: "L'Oreal Paris"})

CREATE (p1:Product {id: 'p_001', name: 'iPhone 15 Pro', price: 1000, commission_rate: 0.05})
CREATE (p2:Product {id: 'p_002', name: 'AirPods Pro 2', price: 250, commission_rate: 0.08})
CREATE (p3:Product {id: 'p_003', name: 'Son M.A.C Ruby Woo', price: 30, commission_rate: 0.15})

CREATE (v1)-[:SELLS]->(p1)
CREATE (v1)-[:SELLS]->(p2)
CREATE (v2)-[:SELLS]->(p3)

CREATE (a1:Affiliate {id: 'aff_001', name: 'Vật Vờ Studio', platform: 'YouTube', followers: 2000000})
CREATE (a2:Affiliate {id: 'aff_002', name: 'Hà Linh Official', platform: 'TikTok', followers: 5000000})

CREATE (a1)-[:PROMOTES {tracking_link: 'bit.ly/vatvo-ip15'}]->(p1)
CREATE (a1)-[:PROMOTES {tracking_link: 'bit.ly/vatvo-airpods'}]->(p2)
CREATE (a2)-[:PROMOTES {tracking_link: 'bit.ly/halinh-sonmac'}]->(p3)

CREATE (c1:Customer {id: 'cus_001', name: 'Nguyễn Văn A', email: 'nva@gmail.com'})
CREATE (c2:Customer {id: 'cus_002', name: 'Trần Thị B', email: 'ttb@gmail.com'})

CREATE (o1:Order {id: 'ord_001', date: '2024-05-10', total_amount: 1000, status: 'Completed'})
CREATE (c1)-[:PLACED]->(o1)
CREATE (o1)-[:CONTAINS {quantity: 1}]->(p1)
CREATE (o1)-[:REFERRED_BY {commission_earned: 50}]->(a1) 

CREATE (o2:Order {id: 'ord_002', date: '2024-05-11', total_amount: 60, status: 'Completed'})
CREATE (c2)-[:PLACED]->(o2)
CREATE (o2)-[:CONTAINS {quantity: 2}]->(p3) 
CREATE (o2)-[:REFERRED_BY {commission_earned: 9}]->(a2) 

CREATE (o3:Order {id: 'ord_003', date: '2024-05-12', total_amount: 30, status: 'Completed'})
CREATE (c1)-[:PLACED]->(o3)
CREATE (o3)-[:CONTAINS {quantity: 1}]->(p3)
CREATE (o3)-[:REFERRED_BY {commission_earned: 4.5}]->(a2)