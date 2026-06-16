# DocX 编辑（无 python-docx）
当 python-docx 不可用时，用 zipfile + XML ElementTree 编辑 .docx。

## 读 docx 文本
```python
import zipfile, xml.etree.ElementTree as ET
with zipfile.ZipFile(path) as z:
    root = ET.fromstring(z.read('word/document.xml'))
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
texts = [t.text for t in root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if t.text]
```

## 写 docx（替换全部内容）
```python
import zipfile, xml.etree.ElementTree as ET, re, os, shutil

def write_docx(body_texts, out_path):
    """body_texts: list of plain-text paragraphs. Creates minimal docx."""
    import xml.sax.saxutils as sax
    NS_W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    
    body = ET.Element(f'{{{NS_W}}}body')
    for para in body_texts:
        p = ET.SubElement(body, f'{{{NS_W}}}p')
        # Handle **bold** markers
        parts = re.split(r'(\*\*[^*]+\*\*)', para)
        for part in parts:
            r = ET.SubElement(p, f'{{{NS_W}}}r')
            if part.startswith('**') and part.endswith('**'):
                rPr = ET.SubElement(r, f'{{{NS_W}}}rPr')
                ET.SubElement(rPr, f'{{{NS_W}}}b')
                t = ET.SubElement(r, f'{{{NS_W}}}t')
                t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
                t.text = part[2:-2]
            else:
                t = ET.SubElement(r, f'{{{NS_W}}}t')
                t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
                t.text = part
    
    tree = ET.ElementTree(body)
    tmp_dir = '/tmp/docx_tmp'
    if os.path.exists(tmp_dir): shutil.rmtree(tmp_dir)
    os.makedirs(tmp_dir)
    
    # Create minimal docx structure
    doc = ET.ElementTree(ET.fromstring(
        '<?xml version="1.0" encoding="UTF-8"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body/></w:document>'
    ))
    doc_root = doc.getroot()
    doc_root.append(body)
    
    os.makedirs(f'{tmp_dir}/word')
    doc.write(f'{tmp_dir}/word/document.xml', xml_declaration=True, encoding='UTF-8')
    
    # Create [Content_Types].xml
    ct = ('<?xml version="1.0" encoding="UTF-8"?>'
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
          '</Types>')
    with open(f'{tmp_dir}/[Content_Types].xml', 'w') as f: f.write(ct)
    
    tmp_out = out_path + '.tmp'
    with zipfile.ZipFile(tmp_out, 'w', zipfile.ZIP_DEFLATED) as zout:
        for root_dir, dirs, files in os.walk(tmp_dir):
            for fname in files:
                zout.write(os.path.join(root_dir, fname),
                           os.path.relpath(os.path.join(root_dir, fname), tmp_dir))
    shutil.move(tmp_out, out_path)
    shutil.rmtree(tmp_dir)
```

## 编辑现有 docx（做文本替换）
```python
# Extract → modify word/document.xml w:t text → repack
tmp_dir = '/tmp/docx_edit'
with zipfile.ZipFile(path, 'r') as z: z.extractall(tmp_dir)
# Edit word/document.xml ...
with zipfile.ZipFile(path+'.new', 'w', zipfile.ZIP_DEFLATED) as zout:
    for root, dirs, files in os.walk(tmp_dir):
        for f in files:
            zout.write(os.path.join(root, f),
                       os.path.relpath(os.path.join(root, f), tmp_dir))
shutil.move(path+'.new', path)
```
