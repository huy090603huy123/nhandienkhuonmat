from aspose.threed import Scene
from aspose.threed.entities import Sphere

# Tạo một đối tượng của lớp Scene
scene = Scene()

# Tạo mô hình Sphere
scene.root_node.create_child_node("Sphere", Sphere())

# Lưu tài liệu cảnh 3D
scene.save("D:\\3D\\material_scene.fbx")
