-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 22-11-2025 a las 03:29:55
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `gestor_asistencia_db`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add alumno', 7, 'add_alumno'),
(26, 'Can change alumno', 7, 'change_alumno'),
(27, 'Can delete alumno', 7, 'delete_alumno'),
(28, 'Can view alumno', 7, 'view_alumno'),
(29, 'Can add apoderado', 8, 'add_apoderado'),
(30, 'Can change apoderado', 8, 'change_apoderado'),
(31, 'Can delete apoderado', 8, 'delete_apoderado'),
(32, 'Can view apoderado', 8, 'view_apoderado'),
(33, 'Can add director', 9, 'add_director'),
(34, 'Can change director', 9, 'change_director'),
(35, 'Can delete director', 9, 'delete_director'),
(36, 'Can view director', 9, 'view_director'),
(37, 'Can add inspector', 10, 'add_inspector'),
(38, 'Can change inspector', 10, 'change_inspector'),
(39, 'Can delete inspector', 10, 'delete_inspector'),
(40, 'Can view inspector', 10, 'view_inspector'),
(41, 'Can add usuario', 11, 'add_usuario'),
(42, 'Can change usuario', 11, 'change_usuario'),
(43, 'Can delete usuario', 11, 'delete_usuario'),
(44, 'Can view usuario', 11, 'view_usuario'),
(45, 'Can add profesor', 12, 'add_profesor'),
(46, 'Can change profesor', 12, 'change_profesor'),
(47, 'Can delete profesor', 12, 'delete_profesor'),
(48, 'Can view profesor', 12, 'view_profesor'),
(49, 'Can add notificacion', 13, 'add_notificacion'),
(50, 'Can change notificacion', 13, 'change_notificacion'),
(51, 'Can delete notificacion', 13, 'delete_notificacion'),
(52, 'Can view notificacion', 13, 'view_notificacion'),
(53, 'Can add curso', 14, 'add_curso'),
(54, 'Can change curso', 14, 'change_curso'),
(55, 'Can delete curso', 14, 'delete_curso'),
(56, 'Can view curso', 14, 'view_curso'),
(57, 'Can add certificado medico', 15, 'add_certificadomedico'),
(58, 'Can change certificado medico', 15, 'change_certificadomedico'),
(59, 'Can delete certificado medico', 15, 'delete_certificadomedico'),
(60, 'Can view certificado medico', 15, 'view_certificadomedico'),
(61, 'Can add asistencia', 16, 'add_asistencia'),
(62, 'Can change asistencia', 16, 'change_asistencia'),
(63, 'Can delete asistencia', 16, 'delete_asistencia'),
(64, 'Can view asistencia', 16, 'view_asistencia'),
(65, 'Can add Auditoría', 17, 'add_auditoria'),
(66, 'Can change Auditoría', 17, 'change_auditoria'),
(67, 'Can delete Auditoría', 17, 'delete_auditoria'),
(68, 'Can view Auditoría', 17, 'view_auditoria');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$600000$cAiuZjnHTMUYy5P65LEzVI$1/1KJmHUiU5Z6mC8RxoXJYoJtWpjQSYuBEG+a73vxfs=', '2025-11-21 13:54:38.125065', 1, 'admin', '', '', '', 1, 1, '2025-11-21 13:54:32.171141');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(7, 'gestorApp', 'alumno'),
(8, 'gestorApp', 'apoderado'),
(16, 'gestorApp', 'asistencia'),
(17, 'gestorApp', 'auditoria'),
(15, 'gestorApp', 'certificadomedico'),
(14, 'gestorApp', 'curso'),
(9, 'gestorApp', 'director'),
(10, 'gestorApp', 'inspector'),
(13, 'gestorApp', 'notificacion'),
(12, 'gestorApp', 'profesor'),
(11, 'gestorApp', 'usuario'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-11-20 14:29:47.342950'),
(2, 'auth', '0001_initial', '2025-11-20 14:29:47.745528'),
(3, 'admin', '0001_initial', '2025-11-20 14:29:47.865632'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-11-20 14:29:47.871969'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-11-20 14:29:47.876004'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-11-20 14:29:47.921839'),
(7, 'auth', '0002_alter_permission_name_max_length', '2025-11-20 14:29:47.966798'),
(8, 'auth', '0003_alter_user_email_max_length', '2025-11-20 14:29:47.976030'),
(9, 'auth', '0004_alter_user_username_opts', '2025-11-20 14:29:47.982089'),
(10, 'auth', '0005_alter_user_last_login_null', '2025-11-20 14:29:48.017942'),
(11, 'auth', '0006_require_contenttypes_0002', '2025-11-20 14:29:48.021241'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2025-11-20 14:29:48.027231'),
(13, 'auth', '0008_alter_user_username_max_length', '2025-11-20 14:29:48.039234'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2025-11-20 14:29:48.049578'),
(15, 'auth', '0010_alter_group_name_max_length', '2025-11-20 14:29:48.058717'),
(16, 'auth', '0011_update_proxy_permissions', '2025-11-20 14:29:48.064485'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2025-11-20 14:29:48.073878'),
(18, 'gestorApp', '0001_initial', '2025-11-20 14:29:49.229781'),
(19, 'gestorApp', '0002_remove_asistencia_profesor_asistencia_autorizado_por_and_more', '2025-11-20 14:29:49.576150'),
(20, 'gestorApp', '0003_alter_usuario_correo', '2025-11-20 14:29:49.643505'),
(21, 'gestorApp', '0004_alter_usuario_correo', '2025-11-20 14:29:49.675038'),
(22, 'sessions', '0001_initial', '2025-11-20 14:29:49.705614'),
(23, 'gestorApp', '0005_auditoria_alter_alumno_options_and_more', '2025-11-20 14:30:14.726881');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('0u3zyfqvbdri9ts0m4f1wngmk0gv90oc', '.eJxVjEEOwiAQRe_C2pAOFASX7nsGMsyAVA0kpV0Z765NutDtf-_9lwi4rSVsPS1hZnERIE6_W0R6pLoDvmO9NUmtrssc5a7Ig3Y5NU7P6-H-HRTs5VvT4HzyVmnQ3mRj_OhAxajZ4DmCdYTZUjZjZIsMSTkgS8ZpGiy4nEm8P88eN94:1vMRbb:jF55-vMMZVxBa3-ZdwWuChuaZFtETkOzidxzIlZ17LQ', '2025-11-21 14:25:19.077922'),
('djimuj8gsbat3ckoctqcdp7qnvz4bl4l', '.eJyrViotLk0sysyPz0xRsjLSgXPz8nOTilKVrJR8E4tiSg0MUlMSFdzz86rAbMOc1ColhNqi_BygwoKi_LTU4vwipVoACzoeEg:1vMVxw:h1vItITIp3YowfDI5PMNhXqAjoimt7uGdBNOci9Ml28', '2025-11-21 19:04:40.217372');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gestorapp_alumno`
--

CREATE TABLE `gestorapp_alumno` (
  `id` bigint(20) NOT NULL,
  `rut` varchar(12) NOT NULL,
  `apoderado_id` bigint(20) DEFAULT NULL,
  `curso_id` bigint(20) NOT NULL,
  `usuario_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `gestorapp_alumno`
--

INSERT INTO `gestorapp_alumno` (`id`, `rut`, `apoderado_id`, `curso_id`, `usuario_id`) VALUES
(1, '12345678-9', 1, 1, 9),
(2, '23456789-0', 2, 1, 11),
(3, '34567890-1', 3, 1, 13),
(4, '45678901-2', 4, 1, 15),
(5, '56789012-3', 5, 2, 17),
(6, '67890123-4', 6, 2, 19),
(7, '78901234-5', 7, 2, 21),
(8, '89012345-6', 8, 2, 23),
(9, '90123456-7', 9, 3, 25),
(10, '01234567-8', 10, 3, 27),
(11, '11234567-9', 11, 3, 29),
(12, '21234567-0', 12, 4, 31),
(13, '31234567-1', 13, 4, 33),
(14, '41234567-2', 14, 4, 35);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gestorapp_apoderado`
--

CREATE TABLE `gestorapp_apoderado` (
  `id` bigint(20) NOT NULL,
  `direccion` varchar(200) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `usuario_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `gestorapp_apoderado`
--

INSERT INTO `gestorapp_apoderado` (`id`, `direccion`, `telefono`, `usuario_id`) VALUES
(1, 'Av. Principal 123', '+56911111111', 8),
(2, 'Calle Los Pinos 456', '+56922222222', 10),
(3, 'Pasaje Las Flores 789', '+56933333333', 12),
(4, 'Av. Los Álamos 321', '+56944444444', 14),
(5, 'Calle Central 654', '+56955555555', 16),
(6, 'Paseo La Paz 987', '+56966666666', 18),
(7, 'Calle Sol 147', '+56977777777', 20),
(8, 'Av. Luna 258', '+56988888888', 22),
(9, 'Pasaje Estrella 369', '+56999999999', 24),
(10, 'Calle Cometa 741', '+56900000000', 26),
(11, 'Av. Norte 852', '+56911122233', 28),
(12, 'Calle Sur 963', '+56922233344', 30),
(13, 'Pasaje Este 159', '+56933344455', 32),
(14, 'Av. Oeste 357', '+56944455566', 34);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gestorapp_asistencia`
--

CREATE TABLE `gestorapp_asistencia` (
  `id` bigint(20) NOT NULL,
  `fecha` date NOT NULL,
  `hora_ingreso` time(6) DEFAULT NULL,
  `hora_salida` time(6) DEFAULT NULL,
  `estado` varchar(20) NOT NULL,
  `observacion` longtext DEFAULT NULL,
  `alumno_id` bigint(20) NOT NULL,
  `autorizado_por_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `gestorapp_asistencia`
--

INSERT INTO `gestorapp_asistencia` (`id`, `fecha`, `hora_ingreso`, `hora_salida`, `estado`, `observacion`, `alumno_id`, `autorizado_por_id`) VALUES
(1, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 1, NULL),
(2, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 2, NULL),
(3, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 3, NULL),
(4, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 4, NULL),
(5, '2025-11-21', NULL, NULL, 'Ausente', 'Registro de prueba', 5, NULL),
(6, '2025-11-21', '08:00:00.000000', '15:34:00.000000', 'Retirado', 'Registro de prueba', 6, NULL),
(7, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 7, NULL),
(8, '2025-11-21', NULL, NULL, 'Ausente', 'Registro de prueba', 8, NULL),
(9, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 9, NULL),
(10, '2025-11-21', '08:00:00.000000', '15:26:00.000000', 'Retirado', 'Registro de prueba', 10, NULL),
(11, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 11, NULL),
(12, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 12, NULL),
(13, '2025-11-21', NULL, NULL, 'Ausente', 'Registro de prueba', 13, NULL),
(14, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 14, NULL),
(15, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 1, NULL),
(16, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 2, NULL),
(17, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 3, NULL),
(18, '2025-11-21', NULL, NULL, 'Ausente', 'Registro de prueba', 4, NULL),
(19, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 5, NULL),
(20, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 6, NULL),
(21, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 7, NULL),
(22, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 8, NULL),
(23, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 9, NULL),
(24, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 10, NULL),
(25, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 11, NULL),
(26, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 12, NULL),
(27, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 13, NULL),
(28, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 14, NULL),
(29, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 1, NULL),
(30, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 2, NULL),
(31, '2025-11-21', NULL, NULL, 'Ausente', 'Registro de prueba', 3, NULL),
(32, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 4, NULL),
(33, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 5, NULL),
(34, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 6, NULL),
(35, '2025-11-21', NULL, NULL, 'Ausente', 'Registro de prueba', 7, NULL),
(36, '2025-11-21', NULL, NULL, 'Ausente', 'Registro de prueba', 8, NULL),
(37, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 9, NULL),
(38, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 10, NULL),
(39, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 11, NULL),
(40, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 12, NULL),
(41, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 13, NULL),
(42, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 14, NULL),
(43, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 1, NULL),
(44, '2025-11-21', NULL, NULL, 'Ausente', 'Registro de prueba', 2, NULL),
(45, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 3, NULL),
(46, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 4, NULL),
(47, '2025-11-21', '08:00:00.000000', '15:54:00.000000', 'Retirado', 'Registro de prueba', 5, NULL),
(48, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 6, NULL),
(49, '2025-11-21', NULL, NULL, 'Ausente', 'Registro de prueba', 7, NULL),
(50, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 8, NULL),
(51, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 9, NULL),
(52, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 10, NULL),
(53, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 11, NULL),
(54, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 12, NULL),
(55, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 13, NULL),
(56, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 14, NULL),
(57, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 1, NULL),
(58, '2025-11-21', NULL, NULL, 'Ausente', 'Registro de prueba', 2, NULL),
(59, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 3, NULL),
(60, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 4, NULL),
(61, '2025-11-21', NULL, NULL, 'Ausente', 'Registro de prueba', 5, NULL),
(62, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 6, NULL),
(63, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 7, NULL),
(64, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 8, NULL),
(65, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 9, NULL),
(66, '2025-11-21', '08:00:00.000000', '15:38:00.000000', 'Retirado', 'Registro de prueba', 10, NULL),
(67, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 11, NULL),
(68, '2025-11-21', '08:00:00.000000', '15:42:00.000000', 'Retirado', 'Registro de prueba', 12, NULL),
(69, '2025-11-21', '08:00:00.000000', NULL, 'Presente', NULL, 13, NULL),
(70, '2025-11-21', NULL, NULL, 'Ausente', 'Registro de prueba', 14, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gestorapp_auditoria`
--

CREATE TABLE `gestorapp_auditoria` (
  `id` bigint(20) NOT NULL,
  `accion` varchar(100) NOT NULL,
  `detalle` longtext NOT NULL,
  `tabla_afectada` varchar(50) NOT NULL,
  `registro_id` int(11) DEFAULT NULL,
  `fecha_hora` datetime(6) NOT NULL,
  `ip_address` char(39) DEFAULT NULL,
  `usuario_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gestorapp_certificadomedico`
--

CREATE TABLE `gestorapp_certificadomedico` (
  `id` bigint(20) NOT NULL,
  `fecha_emision` date NOT NULL,
  `motivo` longtext NOT NULL,
  `archivo_pdf` varchar(100) NOT NULL,
  `validado` tinyint(1) NOT NULL,
  `alumno_id` bigint(20) NOT NULL,
  `apoderado_id` bigint(20) NOT NULL,
  `fecha_subida` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gestorapp_curso`
--

CREATE TABLE `gestorapp_curso` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `profesor_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `gestorapp_curso`
--

INSERT INTO `gestorapp_curso` (`id`, `nombre`, `profesor_id`) VALUES
(1, '1° Medio', 1),
(2, '2° Medio', 2),
(3, '3° Medio', 3),
(4, '4° Medio', 4);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gestorapp_director`
--

CREATE TABLE `gestorapp_director` (
  `id` bigint(20) NOT NULL,
  `oficina` varchar(50) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `usuario_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `gestorapp_director`
--

INSERT INTO `gestorapp_director` (`id`, `oficina`, `telefono`, `usuario_id`) VALUES
(1, 'Dirección Principal', '+56912345678', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gestorapp_inspector`
--

CREATE TABLE `gestorapp_inspector` (
  `id` bigint(20) NOT NULL,
  `turno` varchar(50) NOT NULL,
  `director_id` bigint(20) NOT NULL,
  `usuario_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `gestorapp_inspector`
--

INSERT INTO `gestorapp_inspector` (`id`, `turno`, `director_id`, `usuario_id`) VALUES
(1, 'Mañana', 1, 6),
(2, 'Tarde', 1, 7);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gestorapp_notificacion`
--

CREATE TABLE `gestorapp_notificacion` (
  `id` bigint(20) NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `mensaje` longtext NOT NULL,
  `fecha_envio` datetime(6) NOT NULL,
  `alumno_id` bigint(20) NOT NULL,
  `apoderado_id` bigint(20) DEFAULT NULL,
  `inspector_id` bigint(20) DEFAULT NULL,
  `leida` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `gestorapp_notificacion`
--

INSERT INTO `gestorapp_notificacion` (`id`, `tipo`, `mensaje`, `fecha_envio`, `alumno_id`, `apoderado_id`, `inspector_id`, `leida`) VALUES
(1, 'Atraso', 'Juan Pérez llegó tarde hoy.', '2025-11-21 18:20:39.871109', 1, 1, 1, 0),
(2, 'Atraso', 'Sofía Ramírez llegó tarde hoy.', '2025-11-21 18:20:39.875995', 2, 2, 1, 0),
(3, 'Atraso', 'Diego Castro llegó tarde hoy.', '2025-11-21 18:20:39.877300', 3, 3, 1, 0),
(4, 'Atraso', 'Camila Torres llegó tarde hoy.', '2025-11-21 18:20:39.882642', 4, 4, 1, 0),
(5, 'Atraso', 'Valentina Silva llegó tarde hoy.', '2025-11-21 18:20:39.883884', 5, 5, 1, 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gestorapp_profesor`
--

CREATE TABLE `gestorapp_profesor` (
  `id` bigint(20) NOT NULL,
  `oficina` varchar(50) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `director_id` bigint(20) NOT NULL,
  `usuario_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `gestorapp_profesor`
--

INSERT INTO `gestorapp_profesor` (`id`, `oficina`, `telefono`, `director_id`, `usuario_id`) VALUES
(1, 'Sala 101', '+56987654321', 1, 2),
(2, 'Sala 102', '+56987654321', 1, 3),
(3, 'Sala 103', '+56987654321', 1, 4),
(4, 'Sala 104', '+56987654321', 1, 5);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gestorapp_usuario`
--

CREATE TABLE `gestorapp_usuario` (
  `id` bigint(20) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `correo` varchar(254) NOT NULL,
  `contrasena` varchar(255) NOT NULL,
  `rol` varchar(20) NOT NULL,
  `estado` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `gestorapp_usuario`
--

INSERT INTO `gestorapp_usuario` (`id`, `nombre`, `correo`, `contrasena`, `rol`, `estado`) VALUES
(1, 'Carlos Méndez', 'director@colegio.cl', 'pbkdf2_sha256$600000$WhjmrIxQv16I2OZ47oXaj7$qYoBkXm/koePN1U1t8DdyvRQMq30GSHazdA+GO/mJn0=', 'director', 1),
(2, 'María González', 'maria.gonzalez@colegio.cl', 'pbkdf2_sha256$600000$hkkQL0pupp6cGgM91qPWZA$NPbW1l/64HsAFpX4b7sOgxe+jbwDZh+oDxp0+rVuHaQ=', 'profesor', 1),
(3, 'Pedro Rodríguez', 'pedro.rodriguez@colegio.cl', 'pbkdf2_sha256$600000$dTF9rFwlSzMkTewBHxWXPv$RqaVkAV/XOrVk2zTUuNiKcMnZ+MYCsbXThXdYgd0Dsg=', 'profesor', 1),
(4, 'Ana Martínez', 'ana.martinez@colegio.cl', 'pbkdf2_sha256$600000$uoZW0saiJBV7UdI8Pl4Z3H$KjLX7h2ItKA/jCVrn4LNnk6Z0aTia66U98VIYI4/QeE=', 'profesor', 1),
(5, 'Luis Torres', 'luis.torres@colegio.cl', 'pbkdf2_sha256$600000$TAyT3jZV393Az1cT3keRfD$nt12rjsMUpU2+Gw4H9IJHd8pg2suzyo4y9sIdcJYsXU=', 'profesor', 1),
(6, 'Roberto Sánchez', 'roberto.sanchez@colegio.cl', 'pbkdf2_sha256$600000$TjJOaNA4KzsSCnHxkE3r8J$Eh1jf/z3jpllCOxV6XcCIx26c3qMRDJefGVctpOZGHI=', 'inspector', 1),
(7, 'Carmen López', 'carmen.lopez@colegio.cl', 'pbkdf2_sha256$600000$zr1CPkaiwUPY1BL397wm39$2yACUd4I7bg4zBs9H+PTA3FAjA02SJ5SYUTWlvGRWxo=', 'inspector', 1),
(8, 'María Pérez', 'maria.perez@apoderado.cl', 'pbkdf2_sha256$600000$XHU5ui5RSVtUSEz9TgPYoo$7Mb7IvsQOcWEtuI3911+t4N5BX3pk1fsZWGWBv0YH5U=', 'apoderado', 1),
(9, 'Juan Pérez', 'juan.perez@estudiante.cl', 'pbkdf2_sha256$600000$E9IT2QDIqI8YlikBc8j7f7$1HEYSphP4V8pRjnpRs7bOgNxhuub3quxQ2jZxhUCnno=', 'alumno', 1),
(10, 'Carlos Ramírez', 'carlos.ramirez@apoderado.cl', 'pbkdf2_sha256$600000$RABrjIxwg1vXDJ0QSh6o8O$R7KDbnkOU5igkGMnxHbO9BdgQ8Ey99MYvogv2nxozJU=', 'apoderado', 1),
(11, 'Sofía Ramírez', 'sofia.ramirez@estudiante.cl', 'pbkdf2_sha256$600000$VOCZwsZ84gSaMULQpSXOMo$u/6F6Ga9+d4JapRZZsaavVz6FrH8m7ZWhNI/qYeHJWQ=', 'alumno', 1),
(12, 'Ana Castro', 'ana.castro@apoderado.cl', 'pbkdf2_sha256$600000$6MNTqP4FOlpUgQalQIrnHE$PC11jEEKqFi46XF6wKSw/GlpK2FHiOqsh7vJzJDcdwY=', 'apoderado', 1),
(13, 'Diego Castro', 'diego.castro@estudiante.cl', 'pbkdf2_sha256$600000$usCnIf6W2uBPaDRqnXghTw$fIF5AirIjtfE7EqKtcjCYofkmedHInYtx2qPeC4r9jg=', 'alumno', 1),
(14, 'Jorge Torres', 'jorge.torres@apoderado.cl', 'pbkdf2_sha256$600000$1A8NJGhNVvZS7YUhAoUGHF$7QRaUUjd0laytjuYYjNMIfaSifFFrnMCUppYI8MpLWw=', 'apoderado', 1),
(15, 'Camila Torres', 'camila.torres@estudiante.cl', 'pbkdf2_sha256$600000$EOdhalFc6fUPcfXaop4eo8$hW1OVgbZyQxckyFRxz5H6v5o/XdR4IK3bQLeslm2Lf4=', 'alumno', 1),
(16, 'Patricia Silva', 'patricia.silva@apoderado.cl', 'pbkdf2_sha256$600000$0vEVAPiWoPGc2tUqflHKkJ$56kMy+etX63Lc5zLxDYQp2c7ecwcg8A+c2PC/AzK1X0=', 'apoderado', 1),
(17, 'Valentina Silva', 'valentina.silva@estudiante.cl', 'pbkdf2_sha256$600000$b5YSMSxMXNHthFMOH3P7GV$S+Q9wdMNlrAczVO4m55Xy33C0TIKZ5sr0miXvft73+g=', 'alumno', 1),
(18, 'Roberto Fernández', 'roberto.fernandez@apoderado.cl', 'pbkdf2_sha256$600000$9VdPPQ789bwqIyTrTn8hjr$LM1qPUj3NDxYylPd3Op25ZwJxk+a7kiwElhuX9pC/Rc=', 'apoderado', 1),
(19, 'Matías Fernández', 'matias.fernandez@estudiante.cl', 'pbkdf2_sha256$600000$zbQR026bInuT4wp7f4iTdj$6xwvfYF/DTjnHaQ2szpoDuQpXkvYHZ6asO3XP/odLPs=', 'alumno', 1),
(20, 'Claudia Morales', 'claudia.morales@apoderado.cl', 'pbkdf2_sha256$600000$AsZTgnihxlMaJqkTKvcDp9$CVKKejS9qmja5cqeg1fF11FZ6+3KSrGjFDLRftWQFd4=', 'apoderado', 1),
(21, 'Isidora Morales', 'isidora.morales@estudiante.cl', 'pbkdf2_sha256$600000$mMq2yltF9f4c3pGgwHkiab$pia16gw/xV1hjgR6iBNxebcFMihOu3ySS6jOMqcS22Y=', 'alumno', 1),
(22, 'Fernando Vega', 'fernando.vega@apoderado.cl', 'pbkdf2_sha256$600000$8ICrz6m2ahtvIY4Zog3VIP$jGfYFTlRfXJsEOmA/6JtAFXi0CF4RyM5HaDC6kL56Gs=', 'apoderado', 1),
(23, 'Sebastián Vega', 'sebastian.vega@estudiante.cl', 'pbkdf2_sha256$600000$yDr9C0RuRk57s8VsSiwvvY$7BlmIgK+7o9EActp6NRGETtS2eFlU+QXsGv0wrImYn8=', 'alumno', 1),
(24, 'Mónica Vargas', 'monica.vargas@apoderado.cl', 'pbkdf2_sha256$600000$PcOl0lBMWLhG8Vdk93hr8y$j4euKrPIOXJMYQ9RjNxzsO/bYXU2PSG5PuLf39w5oNw=', 'apoderado', 1),
(25, 'Benjamín Vargas', 'benjamin.vargas@estudiante.cl', 'pbkdf2_sha256$600000$hfzQMO4H9QLGlUxzKvxenH$G71q4LvNY1sp4LKXETXHgUoWGGZ2bBZDrkoMk00BhPo=', 'alumno', 1),
(26, 'Daniel Rojas', 'daniel.rojas@apoderado.cl', 'pbkdf2_sha256$600000$1drBI7KExtQtPwIHWNYH55$5r4z3ZyTXvQ/MvDnjCuasyF/Z38tu3UBOzRkzx4BcHA=', 'apoderado', 1),
(27, 'Martina Rojas', 'martina.rojas@estudiante.cl', 'pbkdf2_sha256$600000$HdNRXpwcyMGue3FtEg3eU4$KH5Eo3uO+4qqhavnHdt24lZiaUeKpJOu6071ozNJT8E=', 'alumno', 1),
(28, 'Andrea Herrera', 'andrea.herrera@apoderado.cl', 'pbkdf2_sha256$600000$Qi3GPtekMNNzzHEHdV9Ln4$8bhvbCa5jdiebarDFr+Vi50zrjEHfNKivYlNhScQNXk=', 'apoderado', 1),
(29, 'Lucas Herrera', 'lucas.herrera@estudiante.cl', 'pbkdf2_sha256$600000$f1GdL0rW3qQXIfB7yg1uZ6$SW/xCwLoAsMUXcY4oSPSVnvTFdtOdYUlTD6SZuNaR2g=', 'alumno', 1),
(30, 'Luis Contreras', 'luis.contreras@apoderado.cl', 'pbkdf2_sha256$600000$miH8Arz81ZUtywuoSYCPHV$E8eHvH8qs9zLi6AZTzxcr6TtaQQuCa/VwuI8VMy+tjw=', 'apoderado', 1),
(31, 'Emma Contreras', 'emma.contreras@estudiante.cl', 'pbkdf2_sha256$600000$vTZbmv2xHD338COhFMW90z$1TJ7gXhan1S/cHUmeOewW19Om0Q4NXm5HZkaKATVRY0=', 'alumno', 1),
(32, 'Carolina Soto', 'carolina.soto@apoderado.cl', 'pbkdf2_sha256$600000$ItNUFFPSObIfru3YKwMnS7$2/rNpJmEpxfzDPoRaZzufLVinNwyNYKJsVQOpAGw4qg=', 'apoderado', 1),
(33, 'Agustín Soto', 'agustin.soto@estudiante.cl', 'pbkdf2_sha256$600000$GQAdlzfc1dDuDkCMc3Epjh$3icivIwvEp7/HezwreRRrKJr26IL1pMzJt4mTfx49dw=', 'alumno', 1),
(34, 'Pablo Muñoz', 'pablo.munoz@apoderado.cl', 'pbkdf2_sha256$600000$Xbb2HpFFPjfAli0X30y430$JDsraUtRgji8poxtAaM2LYLHl6VZR5ivB96D1e/w7Tc=', 'apoderado', 1),
(35, 'Florencia Muñoz', 'florencia.munoz@estudiante.cl', 'pbkdf2_sha256$600000$GTWgYmwzCBMZpiiVYMO6UU$bUANNPEAg0OLd97bFY+ftR7i/r4e+eFv7hKVAN26s98=', 'alumno', 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indices de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indices de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indices de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indices de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indices de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indices de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indices de la tabla `gestorapp_alumno`
--
ALTER TABLE `gestorapp_alumno`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `rut` (`rut`),
  ADD UNIQUE KEY `usuario_id` (`usuario_id`),
  ADD KEY `gestorApp_alumno_apoderado_id_ef00d906_fk_gestorApp_apoderado_id` (`apoderado_id`),
  ADD KEY `gestorApp_alumno_curso_id_b5052be3_fk_gestorApp_curso_id` (`curso_id`);

--
-- Indices de la tabla `gestorapp_apoderado`
--
ALTER TABLE `gestorapp_apoderado`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `gestorapp_asistencia`
--
ALTER TABLE `gestorapp_asistencia`
  ADD PRIMARY KEY (`id`),
  ADD KEY `gestorApp_asistencia_autorizado_por_id_859591e9_fk_gestorApp` (`autorizado_por_id`),
  ADD KEY `gestorApp_a_fecha_b6ed82_idx` (`fecha`,`estado`),
  ADD KEY `gestorApp_a_alumno__7670f6_idx` (`alumno_id`,`fecha`);

--
-- Indices de la tabla `gestorapp_auditoria`
--
ALTER TABLE `gestorapp_auditoria`
  ADD PRIMARY KEY (`id`),
  ADD KEY `gestorApp_a_fecha_h_09e689_idx` (`fecha_hora`),
  ADD KEY `gestorApp_a_usuario_de10b4_idx` (`usuario_id`,`fecha_hora`),
  ADD KEY `gestorApp_a_tabla_a_b72e41_idx` (`tabla_afectada`),
  ADD KEY `gestorApp_a_accion_d21aa3_idx` (`accion`);

--
-- Indices de la tabla `gestorapp_certificadomedico`
--
ALTER TABLE `gestorapp_certificadomedico`
  ADD PRIMARY KEY (`id`),
  ADD KEY `gestorApp_certificad_alumno_id_2bd09e35_fk_gestorApp` (`alumno_id`),
  ADD KEY `gestorApp_certificad_apoderado_id_efd574f0_fk_gestorApp` (`apoderado_id`);

--
-- Indices de la tabla `gestorapp_curso`
--
ALTER TABLE `gestorapp_curso`
  ADD PRIMARY KEY (`id`),
  ADD KEY `gestorApp_curso_profesor_id_67e043c9_fk_gestorApp_profesor_id` (`profesor_id`);

--
-- Indices de la tabla `gestorapp_director`
--
ALTER TABLE `gestorapp_director`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `gestorapp_inspector`
--
ALTER TABLE `gestorapp_inspector`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `usuario_id` (`usuario_id`),
  ADD KEY `gestorApp_inspector_director_id_4d656521_fk_gestorApp` (`director_id`);

--
-- Indices de la tabla `gestorapp_notificacion`
--
ALTER TABLE `gestorapp_notificacion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `gestorApp_notificacion_alumno_id_dac84fd2_fk_gestorApp_alumno_id` (`alumno_id`),
  ADD KEY `gestorApp_notificaci_inspector_id_0427cafa_fk_gestorApp` (`inspector_id`),
  ADD KEY `gestorApp_n_fecha_e_69b46c_idx` (`fecha_envio`),
  ADD KEY `gestorApp_n_apodera_46880d_idx` (`apoderado_id`,`fecha_envio`);

--
-- Indices de la tabla `gestorapp_profesor`
--
ALTER TABLE `gestorapp_profesor`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `usuario_id` (`usuario_id`),
  ADD KEY `gestorApp_profesor_director_id_1c84d794_fk_gestorApp_director_id` (`director_id`);

--
-- Indices de la tabla `gestorapp_usuario`
--
ALTER TABLE `gestorapp_usuario`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `gestorApp_usuario_correo_96746d91_uniq` (`correo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=69;

--
-- AUTO_INCREMENT de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT de la tabla `gestorapp_alumno`
--
ALTER TABLE `gestorapp_alumno`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT de la tabla `gestorapp_apoderado`
--
ALTER TABLE `gestorapp_apoderado`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT de la tabla `gestorapp_asistencia`
--
ALTER TABLE `gestorapp_asistencia`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=71;

--
-- AUTO_INCREMENT de la tabla `gestorapp_auditoria`
--
ALTER TABLE `gestorapp_auditoria`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `gestorapp_certificadomedico`
--
ALTER TABLE `gestorapp_certificadomedico`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `gestorapp_curso`
--
ALTER TABLE `gestorapp_curso`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `gestorapp_director`
--
ALTER TABLE `gestorapp_director`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `gestorapp_inspector`
--
ALTER TABLE `gestorapp_inspector`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `gestorapp_notificacion`
--
ALTER TABLE `gestorapp_notificacion`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `gestorapp_profesor`
--
ALTER TABLE `gestorapp_profesor`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `gestorapp_usuario`
--
ALTER TABLE `gestorapp_usuario`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Filtros para la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Filtros para la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `gestorapp_alumno`
--
ALTER TABLE `gestorapp_alumno`
  ADD CONSTRAINT `gestorApp_alumno_apoderado_id_ef00d906_fk_gestorApp_apoderado_id` FOREIGN KEY (`apoderado_id`) REFERENCES `gestorapp_apoderado` (`id`),
  ADD CONSTRAINT `gestorApp_alumno_curso_id_b5052be3_fk_gestorApp_curso_id` FOREIGN KEY (`curso_id`) REFERENCES `gestorapp_curso` (`id`),
  ADD CONSTRAINT `gestorApp_alumno_usuario_id_29efe986_fk_gestorApp_usuario_id` FOREIGN KEY (`usuario_id`) REFERENCES `gestorapp_usuario` (`id`);

--
-- Filtros para la tabla `gestorapp_apoderado`
--
ALTER TABLE `gestorapp_apoderado`
  ADD CONSTRAINT `gestorApp_apoderado_usuario_id_f5d8541b_fk_gestorApp_usuario_id` FOREIGN KEY (`usuario_id`) REFERENCES `gestorapp_usuario` (`id`);

--
-- Filtros para la tabla `gestorapp_asistencia`
--
ALTER TABLE `gestorapp_asistencia`
  ADD CONSTRAINT `gestorApp_asistencia_alumno_id_aea4a7d9_fk_gestorApp_alumno_id` FOREIGN KEY (`alumno_id`) REFERENCES `gestorapp_alumno` (`id`),
  ADD CONSTRAINT `gestorApp_asistencia_autorizado_por_id_859591e9_fk_gestorApp` FOREIGN KEY (`autorizado_por_id`) REFERENCES `gestorapp_apoderado` (`id`);

--
-- Filtros para la tabla `gestorapp_auditoria`
--
ALTER TABLE `gestorapp_auditoria`
  ADD CONSTRAINT `gestorApp_auditoria_usuario_id_057b7f15_fk_gestorApp_usuario_id` FOREIGN KEY (`usuario_id`) REFERENCES `gestorapp_usuario` (`id`);

--
-- Filtros para la tabla `gestorapp_certificadomedico`
--
ALTER TABLE `gestorapp_certificadomedico`
  ADD CONSTRAINT `gestorApp_certificad_alumno_id_2bd09e35_fk_gestorApp` FOREIGN KEY (`alumno_id`) REFERENCES `gestorapp_alumno` (`id`),
  ADD CONSTRAINT `gestorApp_certificad_apoderado_id_efd574f0_fk_gestorApp` FOREIGN KEY (`apoderado_id`) REFERENCES `gestorapp_apoderado` (`id`);

--
-- Filtros para la tabla `gestorapp_curso`
--
ALTER TABLE `gestorapp_curso`
  ADD CONSTRAINT `gestorApp_curso_profesor_id_67e043c9_fk_gestorApp_profesor_id` FOREIGN KEY (`profesor_id`) REFERENCES `gestorapp_profesor` (`id`);

--
-- Filtros para la tabla `gestorapp_director`
--
ALTER TABLE `gestorapp_director`
  ADD CONSTRAINT `gestorApp_director_usuario_id_38cef161_fk_gestorApp_usuario_id` FOREIGN KEY (`usuario_id`) REFERENCES `gestorapp_usuario` (`id`);

--
-- Filtros para la tabla `gestorapp_inspector`
--
ALTER TABLE `gestorapp_inspector`
  ADD CONSTRAINT `gestorApp_inspector_director_id_4d656521_fk_gestorApp` FOREIGN KEY (`director_id`) REFERENCES `gestorapp_director` (`id`),
  ADD CONSTRAINT `gestorApp_inspector_usuario_id_09176ae9_fk_gestorApp_usuario_id` FOREIGN KEY (`usuario_id`) REFERENCES `gestorapp_usuario` (`id`);

--
-- Filtros para la tabla `gestorapp_notificacion`
--
ALTER TABLE `gestorapp_notificacion`
  ADD CONSTRAINT `gestorApp_notificaci_apoderado_id_d2259e0c_fk_gestorApp` FOREIGN KEY (`apoderado_id`) REFERENCES `gestorapp_apoderado` (`id`),
  ADD CONSTRAINT `gestorApp_notificaci_inspector_id_0427cafa_fk_gestorApp` FOREIGN KEY (`inspector_id`) REFERENCES `gestorapp_inspector` (`id`),
  ADD CONSTRAINT `gestorApp_notificacion_alumno_id_dac84fd2_fk_gestorApp_alumno_id` FOREIGN KEY (`alumno_id`) REFERENCES `gestorapp_alumno` (`id`);

--
-- Filtros para la tabla `gestorapp_profesor`
--
ALTER TABLE `gestorapp_profesor`
  ADD CONSTRAINT `gestorApp_profesor_director_id_1c84d794_fk_gestorApp_director_id` FOREIGN KEY (`director_id`) REFERENCES `gestorapp_director` (`id`),
  ADD CONSTRAINT `gestorApp_profesor_usuario_id_d7e1ea12_fk_gestorApp_usuario_id` FOREIGN KEY (`usuario_id`) REFERENCES `gestorapp_usuario` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
