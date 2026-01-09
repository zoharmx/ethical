# Solución al Error de Vercel

## ❌ Error Actual
```
The name contains invalid characters. Only letters, digits, and underscores are allowed.
Furthermore, the name should not start with a digit.
```

## ✅ Solución

### Opción 1: Cambiar el Nombre del Proyecto (Recomendado)

1. En la pantalla de "New Project" en Vercel:
   - **Project Name**: Cambia de `ethical_framework` a solo **`ethica`** (sin guiones bajos)

2. Verifica que la configuración sea:
   ```
   Framework Preset: Next.js
   Root Directory: web-app
   Build Command: npm run build
   Output Directory: .next
   Install Command: npm install
   ```

3. **Variables de Entorno** (muy importante):
   ```
   GEMINI_API_KEY=AIzaSyBxSQ6GGcujsIqNznxNQjJt-kKG4Wcuogo
   MISTRAL_API_KEY=cqrcNINDiUWdfsRkUk9BBCq52XzphD1V
   DEEPSEEK_API_KEY=sk-181034ba355c4292ad7f149d569ce4e7
   ```

4. Click en **"Deploy"**

---

### Opción 2: Deploy desde CLI (Más Directo)

Si sigues teniendo problemas, usa el CLI de Vercel:

```bash
# 1. Instalar Vercel CLI
npm install -g vercel

# 2. Login
vercel login

# 3. Navegar al directorio web-app
cd web-app

# 4. Deploy con nombre específico
vercel --name ethica --prod

# 5. Cuando te pregunte por las variables de entorno, agrégalas
```

Durante el deploy, cuando te pregunte:
- **Link to existing project?** → No
- **Project name:** → `ethica`
- **Directory:** → Ya estás en `web-app` así que `.`
- **Override settings?** → No

---

### Opción 3: Vercel Dashboard Manual

1. Ve a https://vercel.com/new

2. **Import Git Repository**:
   - Selecciona: `zoharmx/ethical`
   - Click "Import"

3. **Configure Project**:
   ```
   Project Name: ethica
   Framework: Next.js
   Root Directory: web-app
   ```

4. **Build Settings** (expandir si es necesario):
   ```
   Build Command: npm run build
   Output Directory: .next
   Install Command: npm install
   Development Command: npm run dev
   ```

5. **Environment Variables** (click en "Add"):
   ```
   Name: GEMINI_API_KEY
   Value: AIzaSyBxSQ6GGcujsIqNznxNQjJt-kKG4Wcuogo

   Name: MISTRAL_API_KEY
   Value: cqrcNINDiUWdfsRkUk9BBCq52XzphD1V

   Name: DEEPSEEK_API_KEY
   Value: sk-181034ba355c4292ad7f149d569ce4e7
   ```

6. Click **"Deploy"**

---

## 📝 Checklist Pre-Deploy

Antes de hacer deploy, verifica:

- [ ] Nombre del proyecto es solo letras (sin guiones bajos ni especiales)
- [ ] Root Directory está configurado como `web-app`
- [ ] Framework está detectado como `Next.js`
- [ ] Las 3 variables de entorno están configuradas
- [ ] El repositorio GitHub está actualizado

---

## 🎯 Configuración Correcta

**Nombre del Proyecto:**
```
✅ ethica
✅ ethicaai
✅ ethica-web
❌ ethical_framework  (el guion bajo puede causar problemas)
❌ ethica.ai          (el punto no es permitido)
```

**Root Directory:**
```
✅ web-app
❌ .
❌ /web-app
```

**Framework:**
```
✅ Next.js (auto-detectado)
```

---

## 🚀 Después del Deploy Exitoso

Una vez desplegado, obtendrás una URL como:
```
https://ethica-[hash].vercel.app
```

**Prueba estas rutas:**
- Landing: `https://tu-app.vercel.app/`
- Dashboard: `https://tu-app.vercel.app/dashboard`
- API: `https://tu-app.vercel.app/api/analyze`

---

## 🔧 Si Persiste el Error

Si después de cambiar el nombre aún hay errores:

1. **Limpia el cache de Vercel:**
   - En el dashboard → Project Settings → General
   - Scroll down → "Delete Project"
   - Vuelve a importar con el nuevo nombre

2. **Verifica el package.json:**
   ```bash
   cd web-app
   cat package.json | grep name
   ```
   Debe decir: `"name": "ethica-ai-web"`

3. **Re-deploy desde cero:**
   ```bash
   cd web-app
   rm -rf .vercel
   vercel --name ethica --prod
   ```

---

## 🎉 Deploy Exitoso

Cuando veas esto, estará listo:
```
✅ Production: https://ethica-[hash].vercel.app [copied]
```

Prueba la aplicación y verifica que:
- Landing page carga correctamente
- Dashboard es accesible
- Las animaciones funcionan
- El formulario de análisis funciona

---

## 📞 Ayuda Adicional

Si necesitas ayuda:
- **Vercel Docs**: https://vercel.com/docs
- **Next.js Vercel**: https://nextjs.org/docs/deployment
- **Vercel Support**: https://vercel.com/support

---

*Actualizado: 6 de Enero, 2025*
