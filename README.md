# Cloud
Login &amp; Register With Flask Restful and JWT 

### Register
- URL
  - `/fancy/register`
- Method
  - GET
  - POST
- Request Body
  - `name` as `string`
  - `email` as `VARCHAR`
  - `password` as `string`
- Response
  - `"message: Register successfully"`
  - 
### Login
- URL
  - `/fancy/login`
- Method
  - POST
  - 
- Request Body
  - `name` as `string`
  - `email` as `VARCHAR`
  - `password` as `string
- Response
  - `"message: Login Success!!"`

### Gambar
- URL
  - `/fancy/menu`
- Method
  - GET
  - POST
- Request Body
  - `id` as `int`
  - `file` as `blob`
- Response
  - `"message: Successfully uploading files"`

### Result
- URL
  - `/fancy/result`
- Method
  - GET
  - POST
  - 
- Request Body
  - `id` as `int`
  - `jenis` as `string`
  - `konten` as `text`
  - `poin` as `string`
- Response
  - `"message: Result Data Added Successfully!"`<br/>

### Detail
- URL
  - `/fancy/result/1`
- Method
  - GET
  - PUT
  - DELETE
- Request Body
  - `id` as `int`
  - `jenis` as `string`
  - `konten` as `text`
  - `poin` as `string`
- Response
  - `"message: Data Successfully Update!!"`<br/>

