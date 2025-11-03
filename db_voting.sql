-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Oct 17, 2025 at 12:58 AM
-- Server version: 8.0.30
-- PHP Version: 8.2.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_voting`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id_admin` int NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `nama` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id_admin`, `username`, `password`, `nama`) VALUES
(1, 'admin', '$2b$12$KsDbU4KW.xp1T1dg/1sMWuRAW3L4iTEkEl59uCLbAQ431casvFV4e', 'Administrator');

-- --------------------------------------------------------

--
-- Table structure for table `candidates`
--

CREATE TABLE `candidates` (
  `id_candidate` int NOT NULL,
  `nama` varchar(50) NOT NULL,
  `foto` varchar(255) NOT NULL,
  `visi` varchar(255) NOT NULL,
  `misi` text NOT NULL,
  `id_pemilihan` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `candidates`
--

INSERT INTO `candidates` (`id_candidate`, `nama`, `foto`, `visi`, `misi`, `id_pemilihan`) VALUES
(3, 'Safrizal RZ', '5f2d9458e9c94cdca8245d394b4aa31a_banner-xpander-cross.png', 'Menguasai dunia', '1. Menciptakan huru hara\r\n2. Menciptakan benteng terkuat', 1),
(5, 'Gibran', 'f9b7e8d5460b4f6e99eca6d976c04790_aldi.jpg', 'fgsdf', 'sdfgsdfgsdfgsf sdgsdfgs', 1);

-- --------------------------------------------------------

--
-- Table structure for table `kelas`
--

CREATE TABLE `kelas` (
  `id_kelas` int NOT NULL,
  `kode_kelas` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `kelas`
--

INSERT INTO `kelas` (`id_kelas`, `kode_kelas`) VALUES
(1, 'X RPL 1'),
(2, 'X RPL 2'),
(3, 'XI RPL 1');

-- --------------------------------------------------------

--
-- Table structure for table `pemilihan`
--

CREATE TABLE `pemilihan` (
  `id_pemilihan` int NOT NULL,
  `nama_pemilihan` varchar(100) NOT NULL,
  `tanggal_mulai` date NOT NULL,
  `tanggal_selesai` date NOT NULL,
  `status` enum('T','F') NOT NULL,
  `id_admin` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pemilihan`
--

INSERT INTO `pemilihan` (`id_pemilihan`, `nama_pemilihan`, `tanggal_mulai`, `tanggal_selesai`, `status`, `id_admin`) VALUES
(1, 'Pemilihan Ketua OSIS 2025', '2025-10-06', '2025-10-08', 'T', 1);

-- --------------------------------------------------------

--
-- Table structure for table `voters`
--

CREATE TABLE `voters` (
  `id_voter` int NOT NULL,
  `nama` varchar(50) NOT NULL,
  `id_kelas` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `voters`
--

INSERT INTO `voters` (`id_voter`, `nama`, `id_kelas`) VALUES
(2, 'Budi', 1),
(4, 'Safrizal', 1),
(5, 'Andi ', 1),
(6, 'Candra', 2),
(7, 'Endi', 2),
(8, 'Maimunah', 3),
(9, 'Gilbi', 3);

-- --------------------------------------------------------

--
-- Table structure for table `voting`
--

CREATE TABLE `voting` (
  `id_voting` int NOT NULL,
  `verification_code` varchar(5) NOT NULL,
  `id_voter` int DEFAULT NULL,
  `id_pemilihan` int NOT NULL,
  `id_candidate` int NOT NULL,
  `created_at` timestamp NOT NULL,
  `updated_at` timestamp NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `voting`
--

INSERT INTO `voting` (`id_voting`, `verification_code`, `id_voter`, `id_pemilihan`, `id_candidate`, `created_at`, `updated_at`) VALUES
(1, 'ABCDE', 5, 1, 3, '2025-10-17 00:55:57', '2025-10-17 00:55:57'),
(3, 'ABCD1', 2, 1, 5, '2025-10-17 00:57:39', '2025-10-17 00:57:39'),
(4, 'ABCD2', 6, 1, 3, '2025-10-17 00:58:07', '2025-10-17 00:58:07');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id_admin`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `candidates`
--
ALTER TABLE `candidates`
  ADD PRIMARY KEY (`id_candidate`),
  ADD KEY `id_pemilihan` (`id_pemilihan`);

--
-- Indexes for table `kelas`
--
ALTER TABLE `kelas`
  ADD PRIMARY KEY (`id_kelas`);

--
-- Indexes for table `pemilihan`
--
ALTER TABLE `pemilihan`
  ADD PRIMARY KEY (`id_pemilihan`),
  ADD KEY `pemilihan_ibfk_1` (`id_admin`);

--
-- Indexes for table `voters`
--
ALTER TABLE `voters`
  ADD PRIMARY KEY (`id_voter`),
  ADD KEY `id_kelas` (`id_kelas`);

--
-- Indexes for table `voting`
--
ALTER TABLE `voting`
  ADD PRIMARY KEY (`id_voting`),
  ADD UNIQUE KEY `verification_code` (`verification_code`),
  ADD KEY `voting_ibfk_2` (`id_pemilihan`),
  ADD KEY `voting_ibfk_3` (`id_candidate`),
  ADD KEY `voting_ibfk_1` (`id_voter`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id_admin` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `candidates`
--
ALTER TABLE `candidates`
  MODIFY `id_candidate` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `kelas`
--
ALTER TABLE `kelas`
  MODIFY `id_kelas` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `pemilihan`
--
ALTER TABLE `pemilihan`
  MODIFY `id_pemilihan` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `voters`
--
ALTER TABLE `voters`
  MODIFY `id_voter` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `voting`
--
ALTER TABLE `voting`
  MODIFY `id_voting` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `candidates`
--
ALTER TABLE `candidates`
  ADD CONSTRAINT `candidates_ibfk_1` FOREIGN KEY (`id_pemilihan`) REFERENCES `pemilihan` (`id_pemilihan`);

--
-- Constraints for table `pemilihan`
--
ALTER TABLE `pemilihan`
  ADD CONSTRAINT `pemilihan_ibfk_1` FOREIGN KEY (`id_admin`) REFERENCES `admin` (`id_admin`);

--
-- Constraints for table `voters`
--
ALTER TABLE `voters`
  ADD CONSTRAINT `voters_ibfk_1` FOREIGN KEY (`id_kelas`) REFERENCES `kelas` (`id_kelas`);

--
-- Constraints for table `voting`
--
ALTER TABLE `voting`
  ADD CONSTRAINT `voting_ibfk_1` FOREIGN KEY (`id_voter`) REFERENCES `voters` (`id_voter`) ON DELETE SET NULL ON UPDATE SET NULL,
  ADD CONSTRAINT `voting_ibfk_2` FOREIGN KEY (`id_pemilihan`) REFERENCES `pemilihan` (`id_pemilihan`),
  ADD CONSTRAINT `voting_ibfk_3` FOREIGN KEY (`id_candidate`) REFERENCES `candidates` (`id_candidate`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
