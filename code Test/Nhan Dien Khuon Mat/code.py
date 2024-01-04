# Ví dụ mã này trình bày cách đọc cảnh 3D.
from aspose.threed import Scene

# Khởi tạo một đối tượng lớp Scene
scene = Scene()

# Tải tài liệu 3D hiện có
scene.open("D:\\3D\\material_scene.fbx")

for node in scene.root_node.child_nodes:
    entity = node.entity;
    print("{0}", entity.name); 