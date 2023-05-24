/**
 * @name class names
 */

 import csharp

 from File f, Class c
 where f.fromSource() and c.getFile() = f and f.getBaseName() in ["SecurityHeaderSettings.cs", "security.json", "UpdateRolePermissionsRequest.cs","TokenService.cs"]
 select f.getBaseName() as filename, c.getName() as code
