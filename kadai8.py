import random as r
import pygame as pg

def main():

  # 初期化処理
  pg.init() 
  pg.display.set_caption('551の蓬莱ゲーム')
  disp_w, disp_h = 800, 600
  screen = pg.display.set_mode((disp_w,disp_h))
  clock  = pg.time.Clock()
  font   = pg.font.Font(None,24)
  frame  = 0
  point=1500
  exit_flag = False
  gogo1=True
  exit_code = '000'
  gop=551
  face_sp=1
  face_s = pg.Vector2(48,48) # サイズ
  face_r = face_s/2          # 半径
  face_p = pg.Vector2(50,500) # 位置
  face_v = pg.Vector2(20,0)   # 速度
  # face_a = pg.Vector2(0,0.2) # 加速度
  face_img = pg.image.load(f'data/img/tutenkaku.png')
  face_rect = face_img.get_rect(x=disp_w // 2, y=disp_h - 60)
  # 画像の初期速度
  velocity_y = -10  # 上向きに移動する初期速度（負の値）

# 重力（フレームごとに加速度を増加させる）
  gravity = 0.5
  ground_img = pg.image.load(f'data/img/map-ground-center.png')
  ground_s   = pg.Vector2(48,48) 
  theta = 0.0   # 顔の回転角 (deg) を保持する変数

  # 炎エフェクト
  fire_img = pg.image.load(f'data/img/effect-fire.png')
  fire_img = pg.transform.rotozoom(fire_img,180,1) # 180度の回転
  fire_rect = fire_img.get_rect(x=r.randint(0, disp_h - fire_img.get_width()), y=r.randint(-disp_h, 0))

  gg1_img = pg.image.load(f'data/img/butaman.png')
  enemy_img = pg.image.load(f'data/img/tobita.png')
  tako_img = pg.image.load(f'data/img/tako.png')
  gogo1_img = pg.image.load(f'data/img/gogo1.png')
  images = []
  for i in range(10):
    images.append({
    'image': enemy_img,
    'rect': enemy_img.get_rect(x=r.randint(0, disp_h - enemy_img.get_width()), y=r.randint(-disp_h, 0)),
    'speed': r.randint(1, 5),
    'type': 1  # 画像のタイプを識別するための番号
    } )
    images.append({
    'image': gg1_img,
    'rect': gg1_img.get_rect(x=r.randint(0, disp_h - gg1_img.get_width()), y=r.randint(-disp_h, 0)),
    'speed': r.randint(1, 5),
    'type': 2  # 画像のタイプを識別するための番号
    })
  images.append({
    'image': tako_img,
    'rect': tako_img.get_rect(x=r.randint(0, disp_h - tako_img.get_width()), y=r.randint(-disp_h, 0)),
    'speed': r.randint(1, 5),
    'type': 3  # 画像のタイプを識別するための番号
    })
  images.append({
    'image': gogo1_img,
    'rect': gogo1_img.get_rect(x=r.randint(0, disp_h - gogo1_img.get_width()), y=r.randint(-disp_h, 0)),
    'speed': r.randint(1, 5),
    'type': 4  # 画像のタイプを識別するための番号
    })
  attach_condition_met = False
  pg.display.flip()
  damage = 0 # 敵に衝突直後の無敵時間の残りを保持する変数

  # ゲームループ
  while not exit_flag:
    
    # システムイベントの検出
    for event in pg.event.get():
      if event.type == pg.QUIT:
        exit_flag = True
        exit_code = '001'
    
    if frame>point and not attach_condition_met:
        attach_condition_met = True
    # 火のエフェクト処理
    if attach_condition_met :
      fire_rect.x = face_rect.x
      fire_rect.y = face_rect.bottom
      face_v.y = -1

    # 位置と速度の更新
    face_p += face_v
    # 魔理沙の回転角度の計算
    if face_v.x > 0 : 
      theta -= min(20,face_v.magnitude_squared()*2.4)
    else :
      theta += min(20,face_v.magnitude_squared()*2.4)

    keys = pg.key.get_pressed()
    if keys[pg.K_a]:
        face_rect.x -= face_sp
        face_v.x -=face_sp
    if keys[pg.K_d]:
        face_rect.x += face_sp
        face_v.x +=face_sp
    ## 右端と左端との衝突
    if face_p.x + face_r.x > disp_w :
      face_p.x = disp_w - face_r.x
      face_v.x = -0.8 * face_v.x 
    elif face_p.x - face_r.x < 0:
      face_p.x = face_r.x
      face_v.x = -0.8 * face_v.x 

    # 画像の速度に重力を加える
    velocity_y += gravity

    for img in images:
        img['rect'].y += img['speed']  # 画像のY座標を増加させて落下させる
        if img['rect'].top > disp_h:
            # 画像が画面の下に到達したら、位置をリセットする
            if img['type']==4:
              gogo1=True
            img['rect'].x = r.randint(0, disp_w - enemy_img.get_width())
            img['rect'].y = r.randint(-disp_h, 0)
            img['speed'] = r.randint(1, 5)  # 落下速度をリセット
        face_rect = pg.Rect((face_p-face_s/2),face_s)
        if damage==0:
          if img['rect'].colliderect(face_rect):  # 衝突判定
            if img['type']==1:
              damage = 20  # これがゼロになるまで無敵
              gop-=1
            elif img['type']==2:
              gop+=1.5              # face_sp+=0.05
            elif img['type']==3:
              gop=0
            elif img['type']==4 and gogo1:
              gop+=55.1
              gogo1=False
        else:
          damage -= 1  # 無敵時間の残りをデクリメント
    # 背景描画
    screen.fill(pg.Color('#48c0f0'))

    #落下物と火の描画
    for img in images:
        if attach_condition_met :
          screen.blit(fire_img, fire_rect)
        screen.blit(img['image'], img['rect'])

    img = pg.transform.rotozoom(face_img,theta,1) # imgを回転
    tmp_p = face_p - (img.get_rect().center) # 描画開始位置(左上)の計算
    screen.blit(img,tmp_p)
    for x in range(0,disp_w,int(ground_s.x)):
      screen.blit(ground_img,(x,disp_h-ground_s.y))

    # フレームカウンタの描画
    frame += 1
    frm_str = f'frame meter{frame:05}'
    screen.blit(font.render(frm_str,True,'BLACK'),(10,10))

    gop -= 1
    gop=round(gop,1)
    gop_str = f'551point {gop:04}'
    if gop<=100:
      screen.blit(font.render(gop_str,True,'RED'),(10,50))
    else:
      screen.blit(font.render(gop_str,True,'BLACK'),(10,50))
    if gop<=0:
      print(f'game over あなたのポイントは{frame}です。')
      break
    if face_rect.y<=0:
      print('congratulation 無事に通天閣を打ち上げることができました')
      break

    pg.display.flip()
    # 画面の更新と同期
    pg.display.update()
    clock.tick(30)

  # ゲームループ [ここまで]
  pg.quit()
  return exit_code
if __name__ == "__main__":
  code = main()
  print(f'プログラムを「コード{code}」で終了しました。')