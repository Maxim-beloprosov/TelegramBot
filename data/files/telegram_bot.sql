PGDMP     4    )                z            TelegramBot    15.1    15.1     	           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            
           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false                       1262    16398    TelegramBot    DATABASE     �   CREATE DATABASE "TelegramBot" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Russian_Russia.1251';
    DROP DATABASE "TelegramBot";
                postgres    false            �            1259    16448    id_plus_one    SEQUENCE     t   CREATE SEQUENCE public.id_plus_one
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 "   DROP SEQUENCE public.id_plus_one;
       public          postgres    false            �            1259    16435    films    TABLE     �   CREATE TABLE public.films (
    name text NOT NULL,
    type text NOT NULL,
    user_id_recommended integer NOT NULL,
    id integer DEFAULT nextval('public.id_plus_one'::regclass)
);
    DROP TABLE public.films;
       public         heap    postgres    false    218            �            1259    16414    text_messages_from_user    TABLE     �   CREATE TABLE public.text_messages_from_user (
    user_id integer NOT NULL,
    message_id integer NOT NULL,
    message_text text NOT NULL,
    type_films text,
    user_id_for_recommended integer
);
 +   DROP TABLE public.text_messages_from_user;
       public         heap    postgres    false            �            1259    16411    user_recomended    TABLE     [   CREATE TABLE public.user_recomended (
    user_id integer NOT NULL,
    film_id integer
);
 #   DROP TABLE public.user_recomended;
       public         heap    postgres    false            �            1259    16399    users    TABLE     k   CREATE TABLE public.users (
    id integer NOT NULL,
    full_name text,
    full_name_in_telegram text
);
    DROP TABLE public.users;
       public         heap    postgres    false                      0    16435    films 
   TABLE DATA           D   COPY public.films (name, type, user_id_recommended, id) FROM stdin;
    public          postgres    false    217   �                 0    16414    text_messages_from_user 
   TABLE DATA           y   COPY public.text_messages_from_user (user_id, message_id, message_text, type_films, user_id_for_recommended) FROM stdin;
    public          postgres    false    216   .                 0    16411    user_recomended 
   TABLE DATA           ;   COPY public.user_recomended (user_id, film_id) FROM stdin;
    public          postgres    false    215   �                 0    16399    users 
   TABLE DATA           E   COPY public.users (id, full_name, full_name_in_telegram) FROM stdin;
    public          postgres    false    214                     0    0    id_plus_one    SEQUENCE SET     :   SELECT pg_catalog.setval('public.id_plus_one', 40, true);
          public          postgres    false    218            s           2606    16405    users users_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    214               V  x��T[n�P��]�] D~�&fH��?*R��!m>
��"~����4�fvęq�X���O_Ϝ�s�̥K�-���r�cZSE5��rBsz��+K_q�@+ZR�c��ݨ�Q���ni��%�J���� Nx��7�l��|�r���A�Nl�3�E�JK�[��C���Q�zQ�z��	��t��-�P����#�����0�w�~�|��}���8��o-]Is|�]"��H�G꺥B#4�~���MD-$��vH�6Q:C��w	*�P=�^�p+@��Ax��� ���_(��j��-j u��e���r��#v|4�3CX�0E]��Z�A�M�c����F�z�>�"�]��ؾ1t%�IG�KC
�<��;��}���̡Y"}��I&\8�x�3�)��b��dV�+$0�2��L5���J�;,��Vk��6�y����C=[�F�kX!��d�.T����5}�a��n5�K��]�}���d~����t���Z�Ĕ�Qi�s{Xy�ӽ�	'����!<�!��w��KY�[�R����ѽ]a�\����zc7kPlL��sf���1�cb�?�������w���N����k>�1kK�         �   x�mN��0='S�;
$��.���t (�@b�!���
��8T�,��gc�a`�a$l`b�IV�D�K.i��H�F
4tVtDK�><�PsOi��;����z4�d��r�����Vx±M����S\w����Na�/�����(��Ŝ�g�t�Z�1�z��Ա��Xk)�9+��            x������ � �         �   x����JAF띧�'����8�
��MҦaa��5Y�*?� XXi��`9*�����y��l)����r�M��-��M���U�b��X��O���a���	��Hu&��X!��]���5�i@B�>u���;�+�#_9�)k�1���)����K޽�.|Ť�-%�$�s����/�ߨf����w
�R#�ʴV	�-a���v8�����K����1ƶK��     