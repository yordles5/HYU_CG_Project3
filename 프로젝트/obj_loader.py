import glm

obj_meshs = []

# obj 파일 load 및 parsing, 전처리까지
def load_obj(file_path):
    # 파일을 읽고 파싱
    vertices, normals, raw_faces = parse_obj(file_path)
    tri_faces, f3, f4, fmore = triangulate_faces(raw_faces)
    vertex_normals = average_vertex_normals(vertices, normals, tri_faces)
    vertex_data, index_data = flatten_vertex_index(vertices, vertex_normals, tri_faces)

    # 파일 정보 출력
    print(f"Obj file name: {file_path}")
    print(f"Total number of faces: {len(raw_faces)}")
    print(f"Number of faces with 3 vertices : {f3}")
    print(f"Number of faces with 4 vertices : {f4}")
    print(f"Number of faces with more than 4 vertices : {fmore}")

    meshs = {
        'vertices': vertex_data,
        'indices' : index_data,
        'isVao' : False
    }
    obj_meshs.append(meshs)

def parse_obj(file_path):
    vertices = []  # vertex_position
    normals = []   # vertex_normal 정보
    faces = []     # face 정보

    try:
        with open(file_path, 'r') as file:
            for line in file:
                elements = line.strip().split()
                if not elements:
                    continue

                if elements[0] == 'v':
                    vertices.append([float(coord) for coord in elements[1:4]])

                elif elements[0] == 'vn':
                    normals.append([float(coord) for coord in elements[1:4]])

                elif elements[0] == 'f':
                    face = []
                    for vertex in elements[1:]:
                        if '//' in vertex:  # v//vn
                            v_idx, vn_idx = map(int, vertex.split('//'))
                            face.append((v_idx - 1, vn_idx - 1))

                        elif '/' in vertex:
                            parts = vertex.split('/')
                            if len(parts) == 3 and parts[2] != '':
                                # v/vt/vn → vt 무시 v와 vn만 갖고옴
                                v_idx = int(parts[0]) - 1
                                vn_idx = int(parts[2]) - 1
                                face.append((v_idx, vn_idx))
                            elif len(parts) == 2:
                                # v/vt → vt만 있고 vn은 없음
                                v_idx = int(parts[0]) - 1
                                vn_idx = None
                                face.append((v_idx, vn_idx))
                            else:
                                print(f"[경고] 지원되지 않는 face 포맷: {vertex}")
                                break

                        else:
                            # v만 있는 경우
                            v_idx = int(vertex) - 1
                            vn_idx = None
                            face.append((v_idx, vn_idx))
                    else:
                        faces.append(face)

                elif elements[0] in {'vt', 'mtllib', 'usemtl', 'o', 's'}:
                    continue

    except Exception as e:
        print(f"다음 파일을 읽는 데 에러가 발생함 {file_path}: {e}")

    return vertices, normals, faces

# 삼각분할 알고리즘 (fan triangulate), n각형에서 n-2개의 삼각형 face 리스트를 리턴
def triangulate_faces(faces):
    triangles = []
    count_3 = count_4 = count_more = 0

    for face in faces:
        if len(face) == 3:
            triangles.append(face)
            count_3 += 1
        elif len(face) == 4:
            count_4 += 1
            triangles.extend([
                [face[0], face[1], face[2]],
                [face[0], face[2], face[3]]
            ])
        elif len(face) > 4:
            count_more += 1
            for i in range(1, len(face) - 1):
                triangles.append([face[0], face[i], face[i + 1]])
        else:
            print("Invalid: 3개 미만의 vertex로 구성된 face")

    return triangles, count_3, count_4, count_more

def average_vertex_normals(vertices, normals, tri_faces):
    # phong shading을 위해 vertex normal을 구하는 메소드, 인접하는 face의 normal을 평균
     # vn 정보를 무시하고 face normal을 직접 계산
    normal_map = {}

    for face in tri_faces:
        # 각 face의 vertex index 추출
        v0_idx, v1_idx, v2_idx = [v[0] for v in face]

        # 각 vertex 좌표 가져오기
        p0 = glm.vec3(vertices[v0_idx])
        p1 = glm.vec3(vertices[v1_idx])
        p2 = glm.vec3(vertices[v2_idx])

        # face normal 계산 (cross product)
        edge1 = p1 - p0
        edge2 = p2 - p0
        face_normal = glm.normalize(glm.cross(edge1, edge2))

        # 각 vertex에 이 face normal 추가
        for v_idx in [v0_idx, v1_idx, v2_idx]:
            if v_idx not in normal_map:
                normal_map[v_idx] = []
            normal_map[v_idx].append(face_normal)

    # 평균 normal 계산
    averaged = []
    for i in range(len(vertices)):
        if i in normal_map:
            acc = glm.vec3(0)
            for n in normal_map[i]:
                acc += n
            averaged.append(glm.normalize(acc))
        else:
            averaged.append(glm.vec3(0, 0, 0))  # fallback

    return averaged

def flatten_vertex_index(vertices, vertex_normals, tri_faces):
    # 파싱한 v, vn, face를 바탕으로 openGL에서 쓸 수 있는 vertex, index data 생성
    vertex_data = []
    index_data = []
    index_map = {}
    counter = 0

    for face in tri_faces:
        for v_idx, _ in face:
            key = v_idx
            if key not in index_map:
                index_map[key] = counter
                v = vertices[v_idx]
                n = vertex_normals[v_idx]
                vertex_data.extend([*v, n.x, n.y, n.z])
                counter += 1
            index_data.append(index_map[key])
    return vertex_data, index_data


